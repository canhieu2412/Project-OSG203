Giới thiệu
Công cụ này là một plugin được phát triển cho LLM CLI (do Simon Willison phát triển), cho phép tự động hóa các hoạt động quét mạng bằng cách tận dụng chức năng gọi công cụ (tool calling) trong các mô hình ngôn ngữ lớn (LLM). Người dùng có thể mô tả yêu cầu bằng ngôn ngữ tự nhiên, ví dụ: "Phân tích các dịch vụ đang chạy trên địa chỉ IP 192.168.1.1". Mô hình AI sẽ tự động xác định và thực thi các hàm phù hợp, thực hiện chuỗi các bước logic (ví dụ: thu thập thông tin mạng cục bộ, quét ping để phát hiện thiết bị hoạt động, và phân tích dịch vụ), sau đó trả về kết quả được xử lý dưới dạng JSON hoặc văn bản có cấu trúc.
Dự án này là sản phẩm của môn học OSG203 , Nhóm 3. Mục tiêu của dự án là khám phá việc tích hợp trí tuệ nhân tạo vào các công cụ hệ thống, tập trung vào tự động hóa và phân tích an ninh mạng. Nhóm phát triển bao gồm [Danh sách thành viên: Ví dụ - Thành viên 1 (canhieu), Thành viên 2, Thành viên 3].
Đặc Điểm Nổi Bật

Hỗ trợ đa nền tảng: Tích hợp với ipconfig trên Windows, ip addr/ifconfig trên Linux/macOS.
Phân tích kết quả Nmap tự động: Trích xuất thông tin host, cổng mở và dịch vụ dưới dạng JSON.
Tài liệu hóa và tên hàm bằng tiếng Việt để tăng tính dễ tiếp cận.
Tích hợp quét lỗ hổng cơ bản sử dụng các script NSE (Nmap Scripting Engine) của Nmap.
Yêu cầu hệ thống tối thiểu: Python 3.7 trở lên, LLM CLI và Nmap.

Yêu Cầu Hệ Thống

Python: Phiên bản 3.7 hoặc cao hơn.
LLM CLI: Cài đặt qua pip install llm.
Nmap: Công cụ quét mạng cốt lõi (xem hướng dẫn cài đặt bên dưới).
Mô hình AI: Khuyến nghị Gemini 2.5 Flash (nhanh và hiệu quả chi phí) hoặc các mô hình tương thích khác.

Hướng Dẫn Cài Đặt
1. Cài Đặt LLM CLI
bashpip install llm
llm models install gemini  # Hoặc openai cho các mô hình khác
llm keys set google  # Cấu hình khóa API cho Gemini (nếu sử dụng mô hình này)
2. Cài Đặt Nmap

Ubuntu/Debian:
bashsudo apt update && sudo apt install nmap

macOS:
bashbrew install nmap

Windows: Tải và cài đặt từ trang chính thức của Nmap, sau đó thêm thư mục cài đặt vào biến môi trường PATH.

3. Triển Khai Công Cụ

Tải file nmap_ai.py và đặt vào thư mục làm việc hiện tại.
Không yêu cầu cài đặt gói phụ thuộc thêm; công cụ sử dụng các thư viện chuẩn của Python (subprocess, re, json, v.v.).

Hướng Dẫn Sử Dụng
Công cụ được tải động qua cờ --functions trong LLM CLI. Mô hình AI sẽ tự động gọi các hàm dựa trên ngữ cảnh yêu cầu được mô tả.
Cú Pháp Cơ Bản
bashllm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Mô tả yêu cầu của bạn"

Phiên Làm Việc (Session): Sử dụng -s <tên_phiên> để duy trì ngữ cảnh qua các truy vấn liên tiếp (ví dụ: -s phan_tich_mang), giúp tránh lặp lại thông tin.
Đầu Vào Từ Ống Dẫn (Pipe):
bashcat /etc/hosts | llm --functions nmap_ai.py "Thực hiện quét nhanh trên các host này"


Các Hàm Chính (Được Đăng Ký Tự Động)
Dưới đây là bảng tóm tắt các hàm cốt lõi, được mô hình AI gọi dựa trên yêu cầu:










































HàmMô TảVí Dụ Yêu Cầu (Prompt)lay_thong_tin_mang_local()Thu thập thông tin mạng cục bộ (IP, giao diện, dải quét gợi ý)."Thông tin mạng cục bộ?"quet_nmap(muc_tieu, tuy_chon, phan_tich)Quét Nmap tùy chỉnh với tùy chọn nâng cao và phân tích JSON."Quét 192.168.1.1 với -sV, phân tích JSON"quet_nhanh(muc_tieu)Quét nhanh các cổng phổ biến (-T4 -F)."Quét nhanh 123.30.136.246"quet_cang(muc_tieu, cang)Quét các cổng cụ thể (ví dụ: "80,443")."Quét cổng 80,443 trên IP X"quet_dich_vu(muc_tieu, cang)Phát hiện dịch vụ và phiên bản (-sV)."Phân tích dịch vụ trên 123.30.136.246"quet_os(muc_tieu)Phát hiện hệ điều hành (-O, yêu cầu quyền root)."Xác định hệ điều hành của IP X?"quet_ping(muc_tieu)Quét ping để phát hiện host hoạt động (-sn)."Quét ping 192.168.1.0/24"quet_script(muc_tieu, script, cang)Thực thi script NSE của Nmap (ví dụ: "http-title")."Thực thi script http-title trên IP X"quet_lo_hong(muc_tieu, cang)Quét lỗ hổng cơ bản (--script vuln)."Kiểm tra lỗ hổng trên cổng 80"
Ví Dụ Sử Dụng

Quét Chuỗi Trên Mạng Cục Bộ:
bashllm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Thực hiện quét toàn diện mạng cục bộ: lấy thông tin dải quét, phát hiện host hoạt động qua ping, phân tích dịch vụ trên cổng 22,80,443, và trả về JSON thô."
Kết quả: Mô hình AI tự động thực hiện chuỗi các bước và tổng hợp dưới dạng JSON có cấu trúc.
Quét Địa Chỉ IP Công Khai:
bashllm --model gemini/gemini-2.5-flash --functions nmap_ai.py "Phân tích dịch vụ (-sV -Pn) trên địa chỉ 123.30.136.246, phân tích JSON."
(Cờ -Pn bỏ qua kiểm tra ping nếu host không phản hồi.)
Tiếp Tục Phiên Làm Việc:
bashllm --model gemini/gemini-2.5-flash --functions nmap_ai.py -s phan_tich_mang "Dựa trên kết quả trước, kiểm tra lỗ hổng trên các host hoạt động."


Kiểm Thử Độc Lập
Để kiểm tra công cụ mà không sử dụng LLM CLI, chạy lệnh sau:
bashpython nmap_ai.py  # Hiển thị thông tin mạng cục bộ
python nmap_ai.py ping 192.168.1.0/24  # Quét ping (với phân tích JSON)
python nmap_ai.py dich_vu scanme.nmap.org  # Phân tích dịch vụ trên IP thử nghiệm
Lưu Ý Quan Trọng

An Ninh Và Tuân Thủ Pháp Lý: Công cụ chỉ nên được sử dụng trên các mạng nội bộ hoặc mục tiêu được ủy quyền rõ ràng. Việc quét địa chỉ IP không được phép có thể vi phạm các quy định pháp lý liên quan đến an ninh mạng. Các hàm như phát hiện hệ điều hành yêu cầu quyền root/administrator.
Xử Lý Lỗi Thường Gặp:

"No hosts up": Host không phản hồi hoặc bị chặn bởi tường lửa – thêm -Pn vào yêu cầu.
Kết quả AI không chính xác (hiện tượng hallucination): Chỉ định "Trả về JSON thô từ công cụ, không thêm chỉnh sửa" trong yêu cầu.
Công cụ không tải: Xác nhận sự hiện diện của import llm và @llm.hookimpl trong mã nguồn.


Tối Ưu Hóa: Nếu mô hình Gemini tạo ra kết quả không mong muốn, hãy thử chuyển sang mô hình khác như GPT-4o để nâng cao độ chính xác và độ tin cậy.
