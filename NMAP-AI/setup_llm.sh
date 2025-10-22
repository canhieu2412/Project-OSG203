#!/bin/bash
# =========================================
# Script tự động cài đặt:
# - Python + pip (nếu chưa có)
# - llm CLI (Simon Willison)
# - nmap (qua apt)
# - Thiết lập API key (Google, OpenAI)
# =========================================

set -e

echo "🚀 Bắt đầu thiết lập môi trường LLM + Nmap..."
echo "----------------------------------------------"

# --- Kiểm tra Python ---
if ! command -v python3 &> /dev/null; then
    echo "⚙️ Python3 chưa có — đang cài đặt..."
    sudo apt update && sudo apt install -y python3 python3-pip
else
    echo "✅ Python3 có sẵn: $(python3 --version)"
fi

# --- Kiểm tra pip ---
if ! command -v pip &> /dev/null; then
    echo "⚙️ pip chưa có — đang cài đặt..."
    sudo apt install -y python3-pip
else
    echo "✅ pip có sẵn: $(pip --version)"
fi

# --- Kiểm tra llm ---
echo ""
echo "🔍 Kiểm tra llm..."
if ! command -v llm &> /dev/null; then
    echo "⚙️ Chưa có llm — đang cài đặt..."
    pip install llm
else
    echo "✅ llm đã được cài:"
    llm --version
fi

# --- Cài Nmap ---
echo ""
echo "🔍 Kiểm tra nmap..."
if ! command -v nmap &> /dev/null; then
    echo "⚙️ Chưa có nmap — đang cài đặt..."
    sudo apt update && sudo apt install -y nmap
else
    echo "✅ nmap đã có sẵn: $(nmap --version | head -n 1)"
fi

# --- Tạo thư mục cấu hình LLM ---
echo ""
echo "📁 Tạo thư mục cấu hình nếu chưa có..."
mkdir -p ~/.config/llm

# --- Nhập key ---
echo ""
read -p "🔑 Nhập Google API key (để trống nếu bỏ qua): " GOOGLE_KEY
read -p "🔑 Nhập OpenAI API key (để trống nếu bỏ qua): " OPENAI_KEY

# --- Thiết lập key ---
if [ -n "$GOOGLE_KEY" ]; then
    echo "$GOOGLE_KEY" | llm keys set google
    echo "✅ Đã lưu key Google"
fi

if [ -n "$OPENAI_KEY" ]; then
    echo "$OPENAI_KEY" | llm keys set openai
    echo "✅ Đã lưu key OpenAI"
fi

# --- Hiển thị kết quả ---
echo ""
echo "📜 Danh sách provider có key:"
llm keys list || echo "⚠️ Không đọc được danh sách key (kiểm tra llm cài đặt)."

echo ""
echo "✅ Hoàn tất cấu hình LLM + Nmap!"
echo "----------------------------------------------"
