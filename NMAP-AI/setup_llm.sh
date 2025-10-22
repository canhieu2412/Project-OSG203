#!/bin/bash
# =========================================
# Script tự động cài đặt LLM CLI và nhập API key
# Hỗ trợ: Google, OpenAI
# =========================================

set -e

echo "🔍 Kiểm tra llm..."
if ! command -v llm &> /dev/null; then
    echo "⚙️ Chưa có llm — đang cài đặt..."
    pip install llm
else
    echo "✅ llm đã được cài:"
    llm --version
fi

echo ""
echo "📁 Tạo thư mục cấu hình nếu chưa có..."
mkdir -p ~/.config/llm

# --- Nhập key ---
read -p "Nhập Google API key (để trống nếu bỏ qua): " GOOGLE_KEY
read -p "Nhập OpenAI API key (để trống nếu bỏ qua): " OPENAI_KEY

# --- Đặt key qua lệnh llm ---
if [ -n "$GOOGLE_KEY" ]; then
    echo "$GOOGLE_KEY" | llm keys set google
    echo "✅ Đã lưu key Google"
fi

if [ -n "$OPENAI_KEY" ]; then
    echo "$OPENAI_KEY" | llm keys set openai
    echo "✅ Đã lưu key OpenAI"
fi

echo ""
echo "📜 Kiểm tra danh sách provider có key:"
llm keys list

echo ""
echo "✅ Hoàn tất cấu hình LLM!"
