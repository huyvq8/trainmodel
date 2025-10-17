"""
Configuration file for AI Video Marketing System
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
SRC_DIR = BASE_DIR / "src"

# Create directories if they don't exist
for dir_path in [DATA_DIR, MODELS_DIR, OUTPUTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# AI Model Configurations
AI_CONFIG = {
    # Stable Diffusion settings
    "stable_diffusion": {
        "model_id": "runwayml/stable-diffusion-v1-5",
        "scheduler": "DPMSolverMultistepScheduler",
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "width": 512,
        "height": 512,
        "batch_size": 1
    },
    
    # Real-ESRGAN settings
    "real_esrgan": {
        "model_name": "RealESRGAN_x4plus",
        "scale": 4,
        "half_precision": True
    },
    
    # OpenAI settings
    "openai": {
        "model": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    
    # Whisper settings
    "whisper": {
        "model_size": "base",
        "language": "vi",
        "task": "transcribe"
    }
}

# Video Processing Settings
VIDEO_CONFIG = {
    "default_resolution": (1920, 1080),
    "fps": 30,
    "codec": "libx264",
    "bitrate": "5000k",
    "audio_codec": "aac",
    "audio_bitrate": "128k"
}

# Trend Analysis Settings
TREND_CONFIG = {
    "platforms": ["youtube", "tiktok", "instagram"],
    "max_videos_per_keyword": 50,
    "analysis_timeframe": "7d",
    "min_views": 10000,
    "min_likes": 1000
}

# Content Analysis Settings
CONTENT_CONFIG = {
    "min_video_duration": 30,  # seconds
    "max_video_duration": 300,  # seconds
    "extract_frames_interval": 5,  # seconds
    "max_frames_per_video": 20
}

# Marketing Optimization Settings
MARKETING_CONFIG = {
    "target_audience": "18-35",
    "preferred_duration": (30, 60),  # seconds
    "call_to_action_keywords": ["mua ngay", "đặt hàng", "liên hệ", "giá rẻ"],
    "trending_hashtags": ["#trending", "#viral", "#hot", "#mới"]
}

# API Keys (set via environment variables)
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "youtube": os.getenv("YOUTUBE_API_KEY"),
    "tiktok": os.getenv("TIKTOK_API_KEY")
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    "rotation": "1 day",
    "retention": "30 days"
}

