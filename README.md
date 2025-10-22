# Công Cụ Quét Mạng Nmap Tích Hợp Trí Tuệ Nhân Tạo 

Giới thiệu

`nmap_ai.py` là một plugin Python cho LLM CLI (tool-calling) nhằm hỗ trợ quét và phân tích mạng bằng ngôn ngữ tự nhiên. Công cụ sử dụng Nmap để thực hiện quét, rồi dùng mô hình ngôn ngữ lớn để điều phối các bước và trả về kết quả dưới dạng JSON có cấu trúc hoặc văn bản phân tích.

Dự án được phát triển trong khuôn khổ môn OSG203 , Nhóm 3, năm 2025.

Mục tiêu

- Tự động hóa quy trình quét mạng thông qua yêu cầu bằng ngôn ngữ tự nhiên.
- Trích xuất và tiêu chuẩn hóa kết quả Nmap dưới dạng JSON để dễ xử lý tự động.
- Hỗ trợ đa nền tảng (Windows, Linux).

Tính năng chính

- Hỗ trợ thu thập thông tin mạng cục bộ (IP, giao diện, dải quét gợi ý).
- Thực thi nhiều kiểu quét Nmap: nhanh, quét cổng cụ thể, phát hiện dịch vụ/version, OS detection, script NSE, quét lỗ hổng cơ bản.
- Phân tích tự động kết quả Nmap và xuất JSON có cấu trúc.
- Tài liệu, tên hàm và thông báo bằng tiếng Việt để thuận tiện cho người dùng Việt Nam.
- Không cần thư viện bên ngoài ngoài `llm` (đối với tích hợp với LLM CLI) và các thư viện chuẩn Python.

Yêu cầu hệ thống

- Python 3.7 hoặc cao hơn.
- Nmap (cài đặt hệ điều hành).
- LLM CLI (`pip install llm`) để sử dụng tính năng tool-calling với mô hình AI.
- Khóa API cho mô hình AI tương ứng (ví dụ: Google/Gemini hoặc OpenAI).
- Lấy API KEY miễn phí của gemini tại https://aistudio.google.com/api-keys
Cài đặt

1. Cài đặt LLM CLI , NMAP và mô hình :
   chạy lệnh dưới để tự động cài đặt NMAP và config llm

   Trong trường hợp nếu bị lỗi , hãy tạo môi trường ảo trước bằng lệnh :
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   
```
./setup_llm.sh
```
<img width="1190" height="627" alt="image" src="https://github.com/user-attachments/assets/9725d8db-8663-4517-a3e2-e09493c5a16f" />

Sau khi cài hoàn tất thì ta tiến tới bước sử dụng :


Sử dụng

Cú pháp cơ bản (với LLM CLI)
```
llm --model <model> --functions nmap_ai.py "Mô tả yêu cầu bằng ngôn ngữ tự nhiên"
```
Ví dụ:
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Quét và phân tích dịch vụ  trên địa chỉ 123.30.136.246, trả về JSON."
```

Duy trì ngữ cảnh (session)
Sử dụng `-s <tên_phiên>` để giữ ngữ cảnh qua nhiều truy vấn:
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py -s phan_tich_mang "Tiếp tục kiểm tra lỗ hổng trên host vừa phát hiện"
```

Nhận đầu vào từ ống dẫn (pipe)
```
cat /etc/hosts | llm --functions nmap_ai.py "Thực hiện quét nhanh trên các host này"
```

Các hàm chính (được đăng ký để LLM gọi tự động)

| Hàm | Mô tả | Ví dụ prompt |
|-----|-------|--------------|
| `lay_thong_tin_mang_local()` | Thu thập IP, giao diện, gợi ý dải quét | "Thông tin mạng cục bộ?" |
| `quet_nmap(muc_tieu, tuy_chon, phan_tich)` | Quét Nmap với tùy chọn, trả JSON | "Quét 192.168.1.1 với -sV, phân tích JSON" |
| `quet_nhanh(muc_tieu)` | Quét nhanh các cổng phổ biến (-T4 -F) | "Quét nhanh 123.30.136.246" |
| `quet_cang(muc_tieu, cang)` | Quét các cổng cụ thể | "Quét cổng 80,443 trên IP X" |
| `quet_dich_vu(muc_tieu, cang)` | Phát hiện dịch vụ và version (-sV) | "Phân tích dịch vụ trên 123.30.136.246" |
| `quet_os(muc_tieu)` | Phát hiện hệ điều hành (-O), cần quyền root | "Xác định hệ điều hành của IP X?" |
| `quet_ping(muc_tieu)` | Quét ping để phát hiện host hoạt động (-sn) | "Quét ping 192.168.1.0/24" |
| `quet_script(muc_tieu, script, cang)` | Thực thi script NSE (vd: http-title) | "Thực thi script http-title trên IP X" |
| `quet_lo_hong(muc_tieu, cang)` | Quét lỗ hổng cơ bản (`--script vuln`) | "Kiểm tra lỗ hổng trên cổng 80" |
|`quet_nmap(muc_tieu, tuy_chon="", phan_tich=False)` | quét tối ưu cho pentest | quét tối ưu nhất mạng x.x.x.x |

1 số lệnh mẫu 
Quét dịch vụ (model sẽ chọn tool phù hợp)
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Quét và phân tích dịch vụ trên 123.30.136.246"
```

Quét nhanh (tương đương quet_nhanh)
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Quét nhanh (fast scan) trên 123.30.136.246 và tóm tắt kết quả"
```

Quét ping sweep cho dải nội bộ (model có thể gọi lay_thong_tin_mang_local rồi quet_ping)
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Lấy thông tin mạng local và quét ping các host trong dải gợi ý"
```
```
 llm --model gemini/gemini-2.5-flash --functions test.py "mạng local của tôi là gì"
```

Ví dụ thực tế
<img width="1489" height="595" alt="image" src="https://github.com/user-attachments/assets/768f98a9-1ac1-490f-a26f-dd43793b44d1" />
<img width="1497" height="240" alt="image" src="https://github.com/user-attachments/assets/bf9fabf5-02f5-4ff1-a29f-eefae7360fbe" />


- Quét IP công khai (ví dụ dùng `-Pn` để bỏ kiểm tra ping):
```
llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Quét ,phân tích dịch vụ trên 123.30.136.246, trả về JSON."
```
<img width="1513" height="573" alt="image" src="https://github.com/user-attachments/assets/9ba08510-c7ee-4009-88fc-ae49df3af9bc" />



Xử lý lỗi thường gặp

- “No hosts up”: Host không phản hồi hoặc bị chặn; thử thêm `-Pn`.
- Kết quả AI không chính xác (hallucination): Trong prompt yêu cầu “Trả về JSON thô từ công cụ, không thêm chỉnh sửa”.
- Công cụ không tải: Kiểm tra có `import llm` và `@llm.hookimpl` trong mã.

Bảo mật và tuân thủ pháp lý

- Chỉ sử dụng công cụ trên mạng nội bộ hoặc mục tiêu **được ủy quyền rõ ràng**.  
- Quét hệ thống không được phép có thể vi phạm pháp luật.  
- Một số tùy chọn (ví dụ: OS detection) có thể yêu cầu quyền root/administrator.

Gợi ý tối ưu

- Nếu mô hình Gemini cho kết quả không mong muốn, thử chuyển sang mô hình khác (ví dụ OpenAI GPT-4o, nhưng mất tiền =)))))))) ).
- Khi cần kết quả thô và đáng tin cậy, yêu cầu rõ “trả về JSON thô” trong prompt.

Tác giả và liên hệ

- Nhóm phát triển: Nhóm 3, Môn OSG203 (2025).  
- Người liên hệ: canhieu (người đại diện nhóm).

