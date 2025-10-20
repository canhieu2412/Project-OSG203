import subprocess
import shlex
import socket
import re
import platform
import struct
import json

import llm  # Cho --functions

def lay_thong_tin_mang_local():
    """Lấy info mạng local, hỗ trợ Windows."""
    try:
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        primary_ip = s.getsockname()[0]
        s.close()
        
        all_ips = socket.gethostbyname_ex(hostname)[2]
        
        interface_info = []
        scan_ranges = []
        system = platform.system().lower()
        
        if system in ['linux', 'darwin']:
            # ip addr hoặc ifconfig (như cũ)
            try:
                result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    current_interface = None
                    for line in result.stdout.split('\n'):
                        if re.match(r'^\d+:', line):
                            current_interface = line.split(':')[1].strip()
                        elif 'inet ' in line and current_interface:
                            ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', line)
                            if ip_match and not ip_match.group(1).startswith('127.'):
                                ip_addr = ip_match.group(1)
                                cidr = ip_match.group(2)
                                interface_info.append(f"{current_interface}: {ip_addr}/{cidr}")
                                network_range = tinh_dai_mang(ip_addr, cidr)
                                if network_range:
                                    scan_ranges.append(network_range)
            except:
                pass  # Fallback ifconfig nếu cần, nhưng giữ ngắn
        elif system == 'windows':
            try:
                result = subprocess.run(["ipconfig"], capture_output=True, text=True, encoding='cp1252', timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'IPv4 Address' in line:
                            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                            if ip_match and not ip_match.group(1).startswith('127.'):
                                ip_addr = ip_match.group(1)
                                interface_info.append(f"Windows: {ip_addr}/24")  # Default /24
                                scan_ranges.append(f"{ip_addr.rsplit('.',1)[0]}.0/24")
            except:
                pass
        
        response = f"Tên máy: {hostname}\nIP chính: {primary_ip}\n"
        if all_ips:
            response += f"Tất cả IP: {', '.join(all_ips)}\n"
        if interface_info:
            response += "\nGiao diện: " + "; ".join(interface_info) + "\n"
        if scan_ranges:
            response += "Dải quét: " + "; ".join(scan_ranges) + "\n"
        else:
            octets = primary_ip.split('.')
            response += f"Dải gợi ý: {octets[0]}.{octets[1]}.{octets[2]}.0/24\n"
        
        return response + "\nLưu ý: Dùng dải này với quet_ping_nmap."
    except Exception as ex:
        return f"Lỗi: {ex}"

def tinh_dai_mang(ip_addr, cidr):
    """Tính network address đơn giản."""
    try:
        cidr_int = int(cidr)
        ip_int = struct.unpack("!I", socket.inet_aton(ip_addr))[0]
        mask = (0xFFFFFFFF << (32 - cidr_int)) & 0xFFFFFFFF
        network_int = ip_int & mask
        network_addr = socket.inet_ntoa(struct.pack("!I", network_int))
        return f"{network_addr}/{cidr}"
    except:
        return None

def quet_nmap(muc_tieu, tuy_chon="", phan_tich=False):
    """Quét Nmap cơ bản, với tùy chọn parse JSON."""
    cmd_parts = ["nmap"]
    if tuy_chon:
        cmd_parts.extend(shlex.split(tuy_chon))
    cmd_parts.append(muc_tieu)
    
    try:
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=300, check=False)
        if result.returncode != 0:
            return f"Lỗi: {result.stderr}"
        if phan_tich:
            return phan_tich_output_nmap(result.stdout)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Hết thời gian 5 phút."
    except FileNotFoundError:
        return "Chưa cài nmap."
    except Exception as ex:
        return f"Lỗi: {ex}"

def phan_tich_output_nmap(output):
    """Parse đơn giản thành JSON (khác repo gốc)."""
    ket_qua = {"hosts": [], "loi": None}
    try:
        hosts = re.findall(r'Nmap scan report for ([\d\.]+)', output)
        for host in hosts:
            ports_mo = re.findall(r'(\d+)/tcp\s+open\s+(\S+)', output)
            ket_qua["hosts"].append({
                "ip": host,
                "cang_mo": [{"cang": p[0], "dich_vu": p[1]} for p in ports_mo]
            })
        return json.dumps(ket_qua, ensure_ascii=False, indent=2)
    except Exception as ex:
        ket_qua["loi"] = str(ex)
        return json.dumps(ket_qua, ensure_ascii=False, indent=2)

def quet_nhanh(muc_tieu):
    return quet_nmap(muc_tieu, "-T4 -F")

def quet_cang(muc_tieu, cang):
    return quet_nmap(muc_tieu, f"-p {cang}")

def quet_dich_vu(muc_tieu, cang=""):
    tuy_chon = "-sV"
    if cang:
        tuy_chon += f" -p {cang}"
    return quet_nmap(muc_tieu, tuy_chon)

def quet_os(muc_tieu):
    return quet_nmap(muc_tieu, "-O")

def quet_ping(muc_tieu):
    return quet_nmap(muc_tieu, "-sn")

def quet_script(muc_tieu, script, cang=""):
    tuy_chon = f"--script {script}"
    if cang:
        tuy_chon += f" -p {cang}"
    return quet_nmap(muc_tieu, tuy_chon, phan_tich=True)  # Parse luôn cho script

# Thêm hàm vuln đơn giản (độc đáo)
def quet_lo_hong(muc_tieu, cang=""):
    tuy_chon = "--script vuln"
    if cang:
        tuy_chon += f" -p {cang}"
    return quet_nmap(muc_tieu, tuy_chon, phan_tich=True)

@llm.hookimpl
def register_tools(register):
    register(lay_thong_tin_mang_local)
    register(quet_nmap)
    register(quet_nhanh)
    register(quet_cang)
    register(quet_dich_vu)
    register(quet_os)
    register(quet_ping)
    register(quet_script)
    register(quet_lo_hong)

