"""
Create Sample Video for Headphone Demo
Tạo video mẫu cho demo tai nghe
"""
import os
import sys
from pathlib import Path
import json
from datetime import datetime

def create_sample_video_script():
    """Tạo script để tạo video mẫu"""
    
    print("TAO VIDEO MAU CHO DEMO TAI NGHE")
    print("=" * 40)
    
    # Đọc cấu hình demo
    config_file = Path("outputs/headphone_demo_20251017_214847/demo_config.json")
    
    if not config_file.exists():
        print("Khong tim thay file cau hinh demo!")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("Cau hinh nguoi mau:")
    model_config = config["model_config"]
    for key, value in model_config.items():
        print(f"   {key}: {value}")
    
    print(f"\nSan pham: {config['script']['product']}")
    print(f"Thoi luong: {config['script']['duration']} giay")
    
    # Tạo script để chạy pipeline
    script_content = f'''@echo off
echo ========================================
echo DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A
echo ========================================
echo.
echo Cau hinh nguoi mau:
echo    Gioi tinh: {model_config['gender']}
echo    Do tuoi: {model_config['age']}
echo    Dan toc: {model_config['ethnicity']}
echo    Phong cach: {model_config['style']}
echo    Boi canh: {model_config['setting']}
echo    Trang phuc: {model_config['clothing']}
echo.
echo San pham: {config['script']['product']}
echo Thoi luong: {config['script']['duration']} giay
echo.
echo ========================================
echo CAI DAT DEPENDENCIES
echo ========================================
echo.
echo Dang cai dat cac thu vien can thiet...
pip install torch torchvision transformers diffusers opencv-python moviepy pillow numpy requests
echo.
echo ========================================
echo CHAY PIPELINE AI
echo ========================================
echo.
echo Dang tao video voi AI...
python main.py --mode demo --keywords "wireless headphones" "bluetooth earbuds" "premium audio" --product "{config['script']['product']}" --duration {config['script']['duration']}
echo.
echo ========================================
echo HOAN THANH
echo ========================================
echo.
echo Kiem tra thu muc outputs/ de xem ket qua
echo.
pause
'''
    
    # Lưu script
    script_file = Path("create_headphone_video.bat")
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\nDa tao script: {script_file}")
    print("\nDe tao video, chay lenh:")
    print(f"   {script_file}")
    
    return True

def create_mock_video_info():
    """Tạo thông tin video mẫu"""
    
    print("\nTAO THONG TIN VIDEO MAU")
    print("=" * 30)
    
    # Tạo thông tin video mẫu
    video_info = {
        "product": "Premium Wireless Headphones - Model X1",
        "model": {
            "description": "Nam chau A, 25 tuoi, da trang, mat den, toc den",
            "characteristics": {
                "gender": "male",
                "age": "young adult",
                "ethnicity": "asian",
                "skin_tone": "fair",
                "eye_color": "dark",
                "hair_color": "black"
            }
        },
        "video_specs": {
            "duration": 75,
            "resolution": "1920x1080",
            "fps": 30,
            "format": "mp4"
        },
        "sections": [
            {
                "name": "Hook",
                "duration": "0-5s",
                "content": "Ban co biet tai sao nhung nguoi thanh cong luon deo tai nghe cao cap khong?",
                "visual": "Close-up tai nghe tren tai nguoi mau nam chau A"
            },
            {
                "name": "Introduction", 
                "duration": "5-15s",
                "content": "Hom nay toi se review tai nghe Model X1 - san pham dang lam mua lam gio tren thi truong!",
                "visual": "Nguoi mau cam tai nghe, gioi thieu san pham"
            },
            {
                "name": "Features",
                "duration": "15-30s", 
                "content": "Diem noi bat: am thanh cuc ky trong treo voi cong nghe noise cancelling tien tien",
                "visual": "Nguoi mau deo tai nghe, bieu cam hai long"
            },
            {
                "name": "Design",
                "duration": "30-45s",
                "content": "Thiet ke sang trong, deo ca ngay khong moi tai, pin 30 gio su dung lien tuc", 
                "visual": "Close-up thiet ke tai nghe, nguoi mau trong tu the thoai mai"
            },
            {
                "name": "Connectivity",
                "duration": "45-60s",
                "content": "Ket noi Bluetooth 5.0 sieu nhanh, tuong thich moi thiet bi, gia chi 2.5 trieu",
                "visual": "Nguoi mau ket noi voi dien thoai, su dung tai nghe"
            },
            {
                "name": "Call to Action",
                "duration": "60-75s",
                "content": "Dat hang ngay hom nay de duoc giam 20% va tang kem case bao ve cao cap!",
                "visual": "Nguoi mau chi tay ve phia camera, hien thi link mua hang"
            }
        ],
        "platforms": {
            "youtube": {
                "resolution": "1920x1080",
                "duration": "75s",
                "hashtags": ["#tai nghe", "#wireless", "#bluetooth", "#tech review"]
            },
            "tiktok": {
                "resolution": "1080x1920", 
                "duration": "30s",
                "hashtags": ["#tai nghe", "#wireless", "#tech", "#fyp"]
            },
            "instagram": {
                "resolution": "1080x1080",
                "duration": "60s", 
                "hashtags": ["#tai nghe", "#wireless", "#tech", "#lifestyle"]
            }
        },
        "expected_results": {
            "views": 50000,
            "engagement_rate": 0.05,
            "conversion_rate": 0.02
        }
    }
    
    # Lưu thông tin video
    output_dir = Path("outputs/headphone_demo_20251017_214847")
    video_info_file = output_dir / "video_info.json"
    
    with open(video_info_file, 'w', encoding='utf-8') as f:
        json.dump(video_info, f, indent=2, ensure_ascii=False)
    
    print(f"Da tao thong tin video: {video_info_file}")
    
    # Hiển thị thông tin
    print(f"\nTHONG TIN VIDEO:")
    print(f"   San pham: {video_info['product']}")
    print(f"   Nguoi mau: {video_info['model']['description']}")
    print(f"   Thoi luong: {video_info['video_specs']['duration']} giay")
    print(f"   Do phan giai: {video_info['video_specs']['resolution']}")
    print(f"   So phan: {len(video_info['sections'])}")
    
    print(f"\nCAC PHAN VIDEO:")
    for i, section in enumerate(video_info['sections'], 1):
        print(f"   {i}. {section['name']} ({section['duration']}): {section['content']}")
    
    print(f"\nTOI UU CHO CAC PLATFORM:")
    for platform, specs in video_info['platforms'].items():
        print(f"   {platform.upper()}: {specs['resolution']}, {specs['duration']}")
    
    return video_info

def create_quick_demo():
    """Tạo demo nhanh không cần AI"""
    
    print("\nTAO DEMO NHANH (KHONG CAN AI)")
    print("=" * 35)
    
    # Tạo thư mục demo
    demo_dir = Path("outputs/quick_demo")
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    # Tạo file mô tả video
    video_description = f"""
DEMO VIDEO TAI NGHE VOI NGUOI MAU NAM CHAU A
============================================

SAN PHAM: Premium Wireless Headphones - Model X1
NGUOI MAU: Nam chau A, 25 tuoi, da trang, mat den, toc den
THOI LUONG: 75 giay
DO PHAN GIAI: 1920x1080

NOI DUNG VIDEO:
1. Hook (0-5s): "Ban co biet tai sao nhung nguoi thanh cong luon deo tai nghe cao cap khong?"
   - Visual: Close-up tai nghe tren tai nguoi mau nam chau A

2. Introduction (5-15s): "Hom nay toi se review tai nghe Model X1 - san pham dang lam mua lam gio tren thi truong!"
   - Visual: Nguoi mau cam tai nghe, gioi thieu san pham

3. Features (15-30s): "Diem noi bat: am thanh cuc ky trong treo voi cong nghe noise cancelling tien tien"
   - Visual: Nguoi mau deo tai nghe, bieu cam hai long

4. Design (30-45s): "Thiet ke sang trong, deo ca ngay khong moi tai, pin 30 gio su dung lien tuc"
   - Visual: Close-up thiet ke tai nghe, nguoi mau trong tu the thoai mai

5. Connectivity (45-60s): "Ket noi Bluetooth 5.0 sieu nhanh, tuong thich moi thiet bi, gia chi 2.5 trieu"
   - Visual: Nguoi mau ket noi voi dien thoai, su dung tai nghe

6. Call to Action (60-75s): "Dat hang ngay hom nay de duoc giam 20% va tang kem case bao ve cao cap!"
   - Visual: Nguoi mau chi tay ve phia camera, hien thi link mua hang

TOI UU CHO CAC PLATFORM:
- YouTube: 1920x1080, 75s, hashtags: #tai nghe #wireless #bluetooth #tech review
- TikTok: 1080x1920, 30s, hashtags: #tai nghe #wireless #tech #fyp  
- Instagram: 1080x1080, 60s, hashtags: #tai nghe #wireless #tech #lifestyle

MUC TIEU:
- Views: 50,000+
- Engagement rate: 5%+
- Conversion rate: 2%+

DE TAO VIDEO THUC TE:
1. Cai dat dependencies: pip install torch torchvision transformers diffusers opencv-python moviepy
2. Chay pipeline: python main.py --mode demo --keywords "wireless headphones" "bluetooth earbuds" --product "Premium Wireless Headphones" --duration 75
3. Kiem tra ket qua trong thu muc outputs/

TAO BOI: AI Video Marketing System
NGAY: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Lưu mô tả
    description_file = demo_dir / "video_description.txt"
    with open(description_file, 'w', encoding='utf-8') as f:
        f.write(video_description)
    
    print(f"Da tao mo ta video: {description_file}")
    print(f"Thu muc demo: {demo_dir}")
    
    return demo_dir

def main():
    """Main function"""
    
    print("TAO VIDEO MAU CHO DEMO TAI NGHE")
    print("=" * 40)
    
    # Tạo script chạy video
    if create_sample_video_script():
        print("✓ Da tao script tao video")
    
    # Tạo thông tin video
    video_info = create_mock_video_info()
    if video_info:
        print("✓ Da tao thong tin video")
    
    # Tạo demo nhanh
    demo_dir = create_quick_demo()
    if demo_dir:
        print("✓ Da tao demo nhanh")
    
    print(f"\nHOAN THANH!")
    print(f"De tao video thuc te, chay:")
    print(f"   create_headphone_video.bat")
    print(f"\nHoac chay truc tiep:")
    print(f"   python main.py --mode demo --keywords 'wireless headphones' 'bluetooth earbuds' --product 'Premium Wireless Headphones' --duration 75")
    
    print(f"\nKiem tra cac file da tao:")
    print(f"   - create_headphone_video.bat")
    print(f"   - outputs/headphone_demo_*/video_info.json")
    print(f"   - outputs/quick_demo/video_description.txt")

if __name__ == "__main__":
    main()
