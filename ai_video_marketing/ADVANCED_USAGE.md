# 🚀 Advanced Usage Guide - AI Video Marketing System

## 🎯 Các tính năng nâng cao

### 1. **Async Pipeline** - Xử lý bất đồng bộ
Chạy pipeline với hiệu suất tối ưu bằng cách xử lý song song các tác vụ:

```bash
# Chạy async pipeline
python main.py --mode async --keywords "cooking" "fitness" --product "Health Course" --duration 90
```

**Lợi ích:**
- ⚡ Nhanh hơn 2-3 lần so với pipeline thông thường
- 🔄 Xử lý song song trend analysis và model generation
- 💾 Tối ưu memory usage

### 2. **Batch Pipeline** - Xử lý hàng loạt
Tạo nhiều video cùng lúc với các cấu hình khác nhau:

```bash
# Chạy batch pipeline
python main.py --mode batch --keywords "cooking" "fitness" --product "Health Course" --duration 60
```

**Kết quả:**
- Video gốc với từ khóa "cooking", "fitness"
- Video nâng cao với từ khóa "cooking tips", "fitness tips"
- Tự động tạo 2 thư mục output riêng biệt

### 3. **Performance Optimization** - Tối ưu hiệu suất
Kiểm tra và tối ưu hóa hệ thống:

```bash
# Tối ưu hóa hệ thống
python main.py --mode optimize
```

**Tính năng:**
- 📊 Phân tích hiệu suất CPU, RAM, GPU
- 🔧 Tự động tối ưu PyTorch settings
- 📈 Báo cáo chi tiết và khuyến nghị
- 💡 Gợi ý nâng cấp phần cứng

### 4. **Marketing Strategy** - Chiến lược marketing
Tạo chiến lược marketing toàn diện cho video:

```bash
# Tạo marketing strategy
python main.py --mode marketing --video-path "outputs/video.mp4" --product "Cooking Course" --budget 2000
```

**Bao gồm:**
- 📱 Tối ưu cho từng platform (YouTube, TikTok, Instagram, Facebook)
- 💰 Phân bổ ngân sách thông minh
- 📅 Lịch đăng bài tối ưu
- 📊 Metrics và KPI tracking

## 🛠️ Cấu hình nâng cao

### Tùy chỉnh AI Models

Chỉnh sửa `configs/config.py`:

```python
AI_CONFIG = {
    "stable_diffusion": {
        "model_id": "runwayml/stable-diffusion-v1-5",  # Hoặc model khác
        "num_inference_steps": 50,  # Tăng để có chất lượng cao hơn
        "guidance_scale": 7.5,      # Điều chỉnh độ sáng tạo
        "width": 768,               # Độ phân giải cao hơn
        "height": 768,
        "batch_size": 2             # Tăng nếu có VRAM nhiều
    }
}
```

### Tối ưu cho GPU khác nhau

**GTX 1660 SUPER (4GB VRAM):**
```python
"batch_size": 1,
"use_half_precision": True,
"enable_attention_slicing": True,
"enable_vae_slicing": True
```

**RTX 3080 (10GB VRAM):**
```python
"batch_size": 2,
"use_half_precision": True,
"enable_attention_slicing": False,
"enable_vae_slicing": False
```

**RTX 4090 (24GB VRAM):**
```python
"batch_size": 4,
"use_half_precision": False,
"enable_attention_slicing": False,
"enable_vae_slicing": False
```

## 📊 Monitoring và Analytics

### 1. **Performance Monitoring**
```python
from src.performance_optimizer import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Kiểm tra sức khỏe hệ thống
health = optimizer.check_system_health()
print(f"System status: {health['status']}")

# Monitor tài nguyên real-time
resources = optimizer.monitor_system_resources()
print(f"CPU: {resources['cpu_usage']}%, GPU: {resources['gpu_usage']}%")
```

### 2. **Pipeline Status Tracking**
```python
from src.pipeline_manager import PipelineManager

manager = PipelineManager(config)

# Kiểm tra trạng thái pipeline
status = manager.get_pipeline_status(Path("outputs/pipeline_run_20240101_120000"))
print(f"Steps completed: {status['steps_completed']}")
print(f"Files generated: {len(status['files_generated'])}")
```

## 🎨 Tùy chỉnh nội dung

### 1. **Tạo ảnh người mẫu tùy chỉnh**
```python
from src.image_generation import ModelGenerator

generator = ModelGenerator(AI_CONFIG["stable_diffusion"])

# Tạo prompt tùy chỉnh
custom_prompt = generator.create_model_prompts(
    gender="male",
    age="middle aged", 
    ethnicity="caucasian",
    style="professional",
    setting="office",
    clothing="formal"
)

# Tạo ảnh với seed cố định
images = generator.generate_model_photo(
    prompt=custom_prompt,
    num_images=5,
    seed=42  # Seed cố định để tái tạo kết quả
)
```

### 2. **Tùy chỉnh kịch bản**
```python
from src.script_generation import ScriptGenerator

generator = ScriptGenerator(AI_CONFIG["openai"])

# Tạo nhiều biến thể kịch bản
variations = [
    {
        "name": "professional",
        "target_product": "Business Course",
        "duration": 90,
        "tone": "professional"
    },
    {
        "name": "casual", 
        "target_product": "Lifestyle Course",
        "duration": 60,
        "tone": "friendly"
    }
]

scripts = generator.generate_multiple_scripts(
    trend_analysis, content_analysis, variations
)
```

## 🔧 Troubleshooting nâng cao

### 1. **Lỗi CUDA Out of Memory**
```python
# Giảm batch size
AI_CONFIG["stable_diffusion"]["batch_size"] = 1

# Bật memory optimizations
AI_CONFIG["stable_diffusion"]["enable_attention_slicing"] = True
AI_CONFIG["stable_diffusion"]["enable_vae_slicing"] = True

# Sử dụng half precision
AI_CONFIG["stable_diffusion"]["torch_dtype"] = torch.float16
```

### 2. **Tối ưu cho CPU-only**
```python
# Tắt GPU
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Sử dụng CPU optimizations
AI_CONFIG["stable_diffusion"]["torch_dtype"] = torch.float32
AI_CONFIG["stable_diffusion"]["batch_size"] = 1
```

### 3. **Lỗi FFmpeg**
```bash
# Windows
# Tải FFmpeg từ https://ffmpeg.org
# Thêm vào PATH environment variable

# Linux
sudo apt update && sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Kiểm tra
ffmpeg -version
```

## 📈 Scaling và Production

### 1. **Chạy trên Server**
```bash
# Sử dụng nohup để chạy background
nohup python main.py --mode async --keywords "trending" "viral" > output.log 2>&1 &

# Monitor process
ps aux | grep python
tail -f output.log
```

### 2. **Docker Deployment**
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1

# Copy application
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Run application
CMD ["python", "main.py", "--mode", "demo"]
```

### 3. **API Integration**
```python
from flask import Flask, request, jsonify
from main import AIVideoMarketingSystem

app = Flask(__name__)
system = AIVideoMarketingSystem()

@app.route('/create-video', methods=['POST'])
def create_video():
    data = request.json
    result = system.run_full_pipeline(
        keywords=data['keywords'],
        target_product=data['product'],
        video_duration=data['duration']
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## 🎯 Best Practices

### 1. **Tối ưu từ khóa**
- Sử dụng từ khóa trending thực tế
- Kết hợp từ khóa dài và ngắn
- Phân tích competitor keywords

### 2. **Quản lý tài nguyên**
- Monitor GPU temperature
- Sử dụng memory management context
- Clean up sau mỗi pipeline

### 3. **Quality Control**
- Kiểm tra video output trước khi publish
- A/B test different variations
- Track performance metrics

### 4. **Backup và Recovery**
- Backup models và configs
- Lưu trữ outputs quan trọng
- Version control cho scripts

## 🚀 Next Steps

1. **Tích hợp với APIs thực tế** (YouTube, TikTok, Instagram)
2. **Thêm voice synthesis** cho narration
3. **Implement real-time monitoring dashboard**
4. **Tạo web interface** cho dễ sử dụng
5. **Thêm support cho nhiều ngôn ngữ**

---

**Chúc bạn thành công với hệ thống AI Video Marketing!** 🎉
