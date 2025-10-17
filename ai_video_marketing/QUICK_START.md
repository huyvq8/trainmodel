# 🚀 Quick Start Guide - AI Video Marketing System

## ⚡ Bắt đầu nhanh trong 5 phút

### 1. Cài đặt hệ thống
```bash
# Clone repository
git clone https://github.com/huyvq8/trainmodel.git
cd trainmodel/ai_video_marketing

# Chạy setup tự động
python setup.py
```

### 2. Cấu hình API Keys
```bash
# Copy file template
copy env_template.txt .env

# Chỉnh sửa .env và thêm API keys của bạn
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Chạy demo ngay lập tức
```bash
# Kích hoạt virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Chạy demo
python main.py --mode demo
```

## 🎯 Các lệnh cơ bản

### Demo nhanh
```bash
python main.py --mode demo
```

### Tạo video với từ khóa tùy chỉnh
```bash
python main.py --mode custom --keywords "cooking tips" "healthy recipes" --product "Cooking Course"
```

### Tạo video dài hơn
```bash
python main.py --mode full --keywords "fashion" "style" --product "Fashion Brand" --duration 90
```

## 📊 Kết quả bạn sẽ nhận được

Sau khi chạy, trong thư mục `outputs/` bạn sẽ có:

- **📈 Trend Analysis**: Phân tích xu hướng video
- **👤 Model Images**: Ảnh người mẫu AI chân thực
- **📝 Video Script**: Kịch bản chi tiết
- **🎬 Final Videos**: 
  - `final_video_youtube.mp4` (16:9)
  - `final_video_tiktok.mp4` (9:16)
  - `final_video_instagram.mp4` (1:1)
- **📱 Short Clips**: Các clip ngắn cho social media

## 🔧 Xử lý lỗi thường gặp

### Lỗi "No module named 'torch'"
```bash
pip install torch torchvision
```

### Lỗi "FFmpeg not found"
- Windows: Tải từ https://ffmpeg.org và thêm vào PATH
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

### Lỗi "OpenAI API key not found"
- Kiểm tra file `.env`
- Đảm bảo có API key hợp lệ

## 💡 Tips để có kết quả tốt nhất

1. **Chọn từ khóa trending**: Sử dụng từ khóa đang hot
2. **Thời lượng phù hợp**: 30-60 giây cho TikTok, 60-120 giây cho YouTube
3. **Sản phẩm rõ ràng**: Mô tả sản phẩm cụ thể
4. **API keys đầy đủ**: Càng nhiều API keys càng chính xác

## 🎉 Chúc mừng!

Bạn đã có trong tay một hệ thống AI tạo video marketing hoàn chỉnh! 

**Hãy bắt đầu tạo video viral ngay hôm nay!** 🚀
