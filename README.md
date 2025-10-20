Công Cụ Quét Mạng Nmap Tích Hợp Trí Tuệ Nhân Tạo (nmap_ai.py)
Giới thiệu

nmap_ai.py là một plugin Python cho LLM CLI (tool-calling) nhằm hỗ trợ quét và phân tích mạng bằng ngôn ngữ tự nhiên. Công cụ sử dụng Nmap để thực hiện quét, rồi dùng mô hình ngôn ngữ lớn để điều phối các bước và trả về kết quả dưới dạng JSON có cấu trúc hoặc văn bản phân tích.

Dự án được phát triển trong khuôn khổ môn OSG203 (Hệ Điều Hành Mở), Nhóm 3, năm 2025.

Mục tiêu

Tự động hóa quy trình quét mạng thông qua yêu cầu bằng ngôn ngữ tự nhiên.

Trích xuất và tiêu chuẩn hóa kết quả Nmap dưới dạng JSON để dễ xử lý tự động.

Hỗ trợ đa nền tảng (Windows, Linux, macOS).

Tính năng chính

Hỗ trợ thu thập thông tin mạng cục bộ (IP, giao diện, dải quét gợi ý).

Thực thi nhiều kiểu quét Nmap: nhanh, quét cổng cụ thể, phát hiện dịch vụ/version, OS detection, script NSE, quét lỗ hổng cơ bản.

Phân tích tự động kết quả Nmap và xuất JSON có cấu trúc.

Tài liệu, tên hàm và thông báo bằng tiếng Việt để thuận tiện cho người dùng Việt Nam.

Không cần thư viện bên ngoài ngoài llm (đối với tích hợp với LLM CLI) và các thư viện chuẩn Python.

Yêu cầu hệ thống

Python 3.7 hoặc cao hơn.

Nmap (cài đặt hệ điều hành).

LLM CLI (pip install llm) để sử dụng tính năng tool-calling với mô hình AI.

Khóa API cho mô hình AI tương ứng (ví dụ: Google/Gemini hoặc OpenAI).

Cài đặt

Cài đặt LLM CLI và mô hình (ví dụ với Gemini):

pip install llm
llm models install gemini
llm keys set google   # Thiết lập khóa API cho Gemini


Cài đặt Nmap

Ubuntu / Debian:

sudo apt update && sudo apt install nmap


macOS:

brew install nmap


Windows:
Tải installer từ trang chính thức của Nmap và thêm thư mục cài đặt vào PATH.

Triển khai công cụ:

Tải nmap_ai.py vào thư mục làm việc. Không cần cài thêm thư viện Python khác ngoài llm nếu dùng LLM CLI.

Sử dụng
Cú pháp cơ bản (với LLM CLI)
llm --model <model> --functions nmap_ai.py "Mô tả yêu cầu bằng ngôn ngữ tự nhiên"


Ví dụ:

llm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Phân tích dịch vụ (-sV -Pn) trên địa chỉ 123.30.136.246, trả về JSON."

Duy trì ngữ cảnh (session)

Sử dụng -s <tên_phiên> để giữ ngữ cảnh qua nhiều truy vấn:

llm --model gemini/gemini-2.5-flash --functions nmap_ai.py -s phan_tich_mang "Tiếp tục kiểm tra lỗ hổng trên host vừa phát hiện"

Nhận đầu vào từ ống dẫn (pipe)
cat /etc/hosts | llm --functions nmap_ai.py "Thực hiện quét nhanh trên các host này"

Các hàm chính (được đăng ký để LLM gọi tự động)
Hàm	Mô tả	Ví dụ prompt
lay_thong_tin_mang_local()	Thu thập IP, giao diện, gợi ý dải quét	"Thông tin mạng cục bộ?"
quet_nmap(muc_tieu, tuy_chon, phan_tich)	Quét Nmap với tùy chọn, trả JSON	"Quét 192.168.1.1 với -sV, phân tích JSON"
quet_nhanh(muc_tieu)	Quét nhanh các cổng phổ biến (-T4 -F)	"Quét nhanh 123.30.136.246"
quet_cang(muc_tieu, cang)	Quét các cổng cụ thể	"Quét cổng 80,443 trên IP X"
quet_dich_vu(muc_tieu, cang)	Phát hiện dịch vụ và version (-sV)	"Phân tích dịch vụ trên 123.30.136.246"
quet_os(muc_tieu)	Phát hiện hệ điều hành (-O), cần quyền root	"Xác định hệ điều hành của IP X?"
quet_ping(muc_tieu)	Quét ping để phát hiện host hoạt động (-sn)	"Quét ping 192.168.1.0/24"
quet_script(muc_tieu, script, cang)	Thực thi script NSE (vd: http-title)	"Thực thi script http-title trên IP X"
quet_lo_hong(muc_tieu, cang)	Quét lỗ hổng cơ bản (--script vuln)	"Kiểm tra lỗ hổng trên cổng 80"
Ví dụ thực tế

Quét và trả JSON cho mạng cục bộ:

llm --model gemini/gemini-2.5-flash --functions nmap_ai.py \
"Thực hiện quét toàn diện mạng cục bộ: lấy dải quét, phát hiện host qua ping, phân tích dịch vụ trên cổng 22,80,443, và trả về JSON thô."


Quét IP công khai (ví dụ dùng -Pn để bỏ kiểm tra ping):

llm --model gemini/gemini-2.5-flash --functions nmap_ai.py \
"Phân tích dịch vụ (-sV -Pn) trên 123.30.136.246, trả về JSON."

