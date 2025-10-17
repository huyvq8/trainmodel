# 🎬 AI Video Marketing System

Hệ thống AI tạo video marketing tự động hoàn chỉnh - từ phân tích xu hướng đến sản xuất video thành phẩm.

## 🚀 Tính năng chính

### 1. **Phân tích xu hướng thông minh**
- Tìm kiếm video trending trên YouTube, TikTok, Instagram
- Phân tích engagement patterns và viral factors
- Xác định content hooks và emotional triggers

### 2. **Tạo ảnh người mẫu chân thực**
- Sử dụng Stable Diffusion để tạo ảnh người mẫu
- Tùy chỉnh theo giới tính, độ tuổi, dân tộc
- Tạo portfolio đa dạng cho video

### 3. **Phân tích nội dung với ChatGPT**
- Phân tích text, visual và engagement
- Xác định yếu tố thành công của video
- Đưa ra khuyến nghị tối ưu

### 4. **Tạo kịch bản tự động**
- Tạo kịch bản dựa trên xu hướng
- Tối ưu cho từng platform
- Bao gồm production notes và marketing strategy

### 5. **Sản xuất video AI**
- Tạo video từ kịch bản và ảnh người mẫu
- Thêm text overlay, effects, transitions
- Tối ưu cho nhiều platform

### 6. **Chỉnh sửa và tối ưu**
- Lắp ghép video thành phẩm
- Tạo clips ngắn cho social media
- Tối ưu cho YouTube, TikTok, Instagram

## 📋 Yêu cầu hệ thống

### Phần cứng tối thiểu:
- **CPU**: Intel Core i7-10700 (8 cores, 16 threads) hoặc tương đương
- **RAM**: 32GB DDR4
- **GPU**: NVIDIA GTX 1660 SUPER (4GB VRAM) hoặc tương đương
- **Storage**: 50GB trống

### Phần mềm:
- Python 3.8+
- CUDA 11.8+ (cho GPU)
- FFmpeg

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/huyvq8/trainmodel.git
cd trainmodel/ai_video_marketing
```

### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cài đặt FFmpeg
- **Windows**: Tải từ https://ffmpeg.org/download.html
- **Linux**: `sudo apt install ffmpeg`
- **Mac**: `brew install ffmpeg`

### 5. Cấu hình API Keys
Tạo file `.env` trong thư mục gốc:
```env
OPENAI_API_KEY=your_openai_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
TIKTOK_API_KEY=your_tiktok_api_key_here
```

## 🎯 Sử dụng

### Chạy Demo nhanh
```bash
python main.py --mode demo
```

### Chạy với từ khóa tùy chỉnh
```bash
python main.py --mode custom --keywords "cooking tips" "healthy recipes" --product "Cooking Course" --duration 60
```

### Chạy pipeline đầy đủ
```bash
python main.py --mode full --keywords "fashion" "style" "trending" --product "Fashion Brand" --duration 90 --output ./my_videos
```

## 📁 Cấu trúc dự án

```
ai_video_marketing/
├── src/
│   ├── image_generation/     # Tạo ảnh người mẫu
│   ├── trend_analysis/       # Phân tích xu hướng
│   ├── content_analysis/     # Phân tích nội dung
│   ├── script_generation/    # Tạo kịch bản
│   ├── video_production/     # Sản xuất video
│   └── video_editing/        # Chỉnh sửa video
├── configs/                  # Cấu hình hệ thống
├── data/                     # Dữ liệu đầu vào
├── models/                   # AI models
├── outputs/                  # Kết quả đầu ra
├── tools/                    # Công cụ hỗ trợ
├── main.py                   # File chính
├── requirements.txt          # Dependencies
└── README.md                 # Hướng dẫn
```

## 🔧 Cấu hình nâng cao

### Tùy chỉnh AI models
Chỉnh sửa `configs/config.py`:
```python
AI_CONFIG = {
    "stable_diffusion": {
        "model_id": "runwayml/stable-diffusion-v1-5",
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        # ... các tham số khác
    }
}
```

### Tùy chỉnh video settings
```python
VIDEO_CONFIG = {
    "default_resolution": (1920, 1080),
    "fps": 30,
    "codec": "libx264",
    "bitrate": "5000k",
    # ... các tham số khác
}
```

## 📊 Kết quả đầu ra

Sau khi chạy pipeline, bạn sẽ có:

### 1. **Trend Analysis**
- `trend_analysis.json`: Phân tích xu hướng chi tiết
- Danh sách video trending với metrics

### 2. **Content Analysis**
- `content_analysis/`: Phân tích nội dung từng video
- Insights về viral factors và engagement

### 3. **Model Images**
- `model_images/`: Portfolio ảnh người mẫu
- Nhiều biến thể và góc chụp

### 4. **Video Script**
- `video_script.json`: Kịch bản chi tiết
- Production notes và marketing strategy

### 5. **Final Videos**
- `final_video_youtube.mp4`: Tối ưu cho YouTube
- `final_video_tiktok.mp4`: Tối ưu cho TikTok (9:16)
- `final_video_instagram.mp4`: Tối ưu cho Instagram (1:1)

### 6. **Short Clips**
- `short_clips/`: Các clip ngắn cho social media
- Hook, key points, CTA riêng biệt

## 🎨 Tùy chỉnh nâng cao

### Tạo ảnh người mẫu tùy chỉnh
```python
from src.image_generation.model_generator import ModelGenerator

generator = ModelGenerator(AI_CONFIG["stable_diffusion"])

# Tạo prompt tùy chỉnh
prompt = generator.create_model_prompts(
    gender="male",
    age="middle aged",
    ethnicity="caucasian",
    style="professional",
    setting="office",
    clothing="formal"
)

# Tạo ảnh
images = generator.generate_model_photo(prompt, num_images=5)
```

### Phân tích xu hướng tùy chỉnh
```python
from src.trend_analysis.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer(TREND_CONFIG)

# Tìm kiếm với từ khóa tùy chỉnh
videos = analyzer.search_trending_keywords(
    ["your", "custom", "keywords"], 
    max_results=100
)

# Phân tích patterns
analysis = analyzer.analyze_trending_patterns(videos)
```

## 🚨 Xử lý lỗi thường gặp

### 1. **Lỗi CUDA/GPU**
```bash
# Kiểm tra CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Nếu không có GPU, chạy với CPU
export CUDA_VISIBLE_DEVICES=""
```

### 2. **Lỗi FFmpeg**
```bash
# Kiểm tra FFmpeg
ffmpeg -version

# Cài đặt lại nếu cần
pip install ffmpeg-python
```

### 3. **Lỗi API Keys**
- Kiểm tra file `.env`
- Đảm bảo API keys hợp lệ
- Kiểm tra quota và billing

### 4. **Lỗi memory**
- Giảm batch size trong config
- Sử dụng CPU thay vì GPU
- Tăng virtual memory

## 📈 Tối ưu hiệu suất

### 1. **GPU Optimization**
```python
# Trong config.py
AI_CONFIG["stable_diffusion"]["batch_size"] = 1  # Giảm nếu thiếu VRAM
AI_CONFIG["stable_diffusion"]["half_precision"] = True  # Sử dụng FP16
```

### 2. **Memory Management**
```python
# Clear cache sau mỗi bước
torch.cuda.empty_cache()
```

### 3. **Parallel Processing**
```python
# Xử lý song song khi có thể
from concurrent.futures import ThreadPoolExecutor
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🆘 Hỗ trợ

- **Issues**: Tạo issue trên GitHub
- **Discussions**: Thảo luận trong Discussions
- **Email**: support@example.com

## 🎉 Chúc mừng!

Bạn đã có trong tay một hệ thống AI video marketing hoàn chỉnh! Hãy bắt đầu tạo những video viral ngay hôm nay.

---

**Lưu ý**: Hệ thống này sử dụng AI để tạo nội dung. Hãy đảm bảo tuân thủ các quy định về bản quyền và sử dụng có trách nhiệm.

