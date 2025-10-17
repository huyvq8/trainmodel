# 🎧 Headphone Demo Guide - Người mẫu nam châu Á

## 📋 Tổng quan Demo

Demo này tạo video marketing cho **Premium Wireless Headphones - Model X1** với người mẫu nam châu Á theo yêu cầu:
- **Giới tính**: Nam
- **Dân tộc**: Châu Á  
- **Đặc điểm**: Da trắng, mắt đen, tóc đen
- **Độ tuổi**: 25 tuổi (young adult)
- **Phong cách**: Professional, casual smart

## 🎯 Cấu hình Demo

### Người mẫu
```json
{
  "gender": "male",
  "age": "young adult",
  "ethnicity": "asian", 
  "style": "professional",
  "setting": "studio",
  "clothing": "casual smart"
}
```

### Sản phẩm
- **Tên**: Premium Wireless Headphones - Model X1
- **Thời lượng video**: 75 giây
- **Keywords**: wireless headphones, bluetooth earbuds, noise cancelling, premium audio, tech review

### Kịch bản (6 phần)

#### 1. Hook (0-5s)
- **Lời thoại**: "Bạn có biết tại sao những người thành công luôn đeo tai nghe cao cấp không?"
- **Visual**: Close-up tai nghe trên tai người mẫu nam châu Á

#### 2. Introduction (5-15s)  
- **Lời thoại**: "Hôm nay tôi sẽ review tai nghe Model X1 - sản phẩm đang làm mưa làm gió trên thị trường!"
- **Visual**: Người mẫu cầm tai nghe, giới thiệu sản phẩm

#### 3. Features (15-30s)
- **Lời thoại**: "Điểm nổi bật: âm thanh cực kỳ trong trẻo với công nghệ noise cancelling tiên tiến"
- **Visual**: Người mẫu đeo tai nghe, biểu cảm hài lòng

#### 4. Design (30-45s)
- **Lời thoại**: "Thiết kế sang trọng, đeo cả ngày không mỏi tai, pin 30 giờ sử dụng liên tục"
- **Visual**: Close-up thiết kế tai nghe, người mẫu trong tư thế thoải mái

#### 5. Connectivity (45-60s)
- **Lời thoại**: "Kết nối Bluetooth 5.0 siêu nhanh, tương thích mọi thiết bị, giá chỉ 2.5 triệu"
- **Visual**: Người mẫu kết nối với điện thoại, sử dụng tai nghe

#### 6. Call to Action (60-75s)
- **Lời thoại**: "Đặt hàng ngay hôm nay để được giảm 20% và tặng kèm case bảo vệ cao cấp!"
- **Visual**: Người mẫu chỉ tay về phía camera, hiển thị link mua hàng

## 🚀 Cách chạy Demo

### Bước 1: Tạo cấu hình demo
```bash
python headphone_demo.py
```

### Bước 2: Chạy demo với dependencies
```bash
python run_headphone_demo.py
```

### Bước 3: Hoặc chạy trực tiếp
```bash
# Cài đặt dependencies
pip install torch torchvision transformers diffusers opencv-python moviepy

# Chạy pipeline
python main.py --mode demo --keywords "wireless headphones" "bluetooth earbuds" --product "Premium Wireless Headphones" --duration 75
```

## 📱 Tối ưu Multi-Platform

### YouTube (75s, 1920x1080)
- **Hashtags**: #tai nghe #wireless #bluetooth #tech review #premium audio
- **Thời gian đăng**: 20:00-22:00
- **Ngân sách**: 600 USD (40%)

### TikTok (30s, 1080x1920)  
- **Hashtags**: #tai nghe #wireless #tech #fyp #viral
- **Thời gian đăng**: 18:00-21:00
- **Ngân sách**: 450 USD (30%)

### Instagram (60s, 1080x1080)
- **Hashtags**: #tai nghe #wireless #tech #lifestyle #premium  
- **Thời gian đăng**: 19:00-21:00
- **Ngân sách**: 300 USD (20%)

## 🎨 Custom Prompts cho AI

### Prompt 1 (Studio Professional)
```
Asian male model, 25 years old, black hair, dark eyes, fair skin, wearing wireless headphones, professional studio photography, clean background, modern tech aesthetic, confident expression
```

### Prompt 2 (Lifestyle)
```
Young Asian man, black hair, dark eyes, light skin tone, wearing premium wireless earbuds, tech lifestyle photography, minimalist style, natural lighting
```

### Prompt 3 (Product Focus)
```
Asian male, early 20s, black hair, dark eyes, wearing noise-cancelling headphones, casual pose, modern lifestyle, clean studio lighting, professional headshot
```

### Prompt 4 (Commercial)
```
Handsome Asian man, black hair, dark eyes, fair complexion, wearing high-end wireless headphones, studio portrait, tech product photography, commercial style
```

## 📊 Kết quả mong đợi

### Video Outputs
- `main_video.mp4` - Video chính 75 giây
- `final_video_youtube.mp4` - Tối ưu cho YouTube
- `final_video_tiktok.mp4` - Tối ưu cho TikTok (9:16)
- `final_video_instagram.mp4` - Tối ưu cho Instagram (1:1)

### Model Images
- Portfolio ảnh người mẫu nam châu Á
- Nhiều góc chụp và biểu cảm
- Chất lượng cao, chân thực

### Short Clips
- Hook clip (0-5s)
- Features clip (15-30s)  
- CTA clip (60-75s)

## 🎯 Đối tượng mục tiêu

- **Giới tính**: Nam
- **Độ tuổi**: 18-35 tuổi
- **Sở thích**: Quan tâm đến công nghệ, âm thanh
- **Thu nhập**: Trung bình trở lên
- **Hành vi**: Thích review sản phẩm, mua sắm online

## 📈 Metrics thành công

- **Views**: 50,000+
- **Engagement rate**: 5%+
- **Conversion rate**: 2%+
- **Cost per acquisition**: <50 USD

## 🔧 Troubleshooting

### Lỗi encoding trên Windows
- Sử dụng `headphone_demo.py` thay vì `demo_headphone.py`
- Không dùng emoji trong script

### Lỗi dependencies
```bash
pip install torch torchvision transformers diffusers opencv-python moviepy pillow numpy requests
```

### Lỗi FFmpeg
- Windows: Tải từ https://ffmpeg.org và thêm vào PATH
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

## 📁 File Structure

```
outputs/headphone_demo_YYYYMMDD_HHMMSS/
├── demo_config.json          # Cấu hình demo
├── demo_summary.json         # Tổng hợp demo
├── run_demo.bat             # Batch script
├── trend_analysis/          # Phân tích xu hướng
├── model_images/            # Ảnh người mẫu
├── scripts/                 # Kịch bản
├── main_video.mp4          # Video chính
├── final_video_youtube.mp4 # Video YouTube
├── final_video_tiktok.mp4  # Video TikTok
├── final_video_instagram.mp4 # Video Instagram
└── short_clips/            # Clips ngắn
```

## 🎉 Kết luận

Demo này tạo ra một video marketing hoàn chỉnh cho tai nghe với người mẫu nam châu Á theo đúng yêu cầu. Hệ thống sẽ tự động:

1. ✅ Tạo ảnh người mẫu nam châu Á chân thực
2. ✅ Phân tích xu hướng tai nghe
3. ✅ Tạo kịch bản 75 giây
4. ✅ Sản xuất video với AI
5. ✅ Tối ưu cho 3 platform
6. ✅ Tạo clips ngắn cho social media
7. ✅ Chiến lược marketing toàn diện

**Hệ thống sẵn sàng tạo video viral cho tai nghe!** 🚀
