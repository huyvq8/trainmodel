"""
Simple demo script for headphone product with Asian male model
"""
import sys
from pathlib import Path
import json
from datetime import datetime

def create_headphone_demo_config():
    """Tạo cấu hình demo cho tai nghe"""
    
    print("DEMO: Tao video marketing cho tai nghe voi nguoi mau nam chau A")
    print("=" * 60)
    
    # Cấu hình người mẫu nam châu Á
    model_config = {
        "gender": "male",
        "age": "young adult",  # 20-30 tuổi
        "ethnicity": "asian",
        "style": "professional",
        "setting": "studio",
        "clothing": "casual smart"
    }
    
    # Keywords cho tai nghe
    keywords = [
        "wireless headphones",
        "bluetooth earbuds", 
        "noise cancelling",
        "premium audio",
        "tech review"
    ]
    
    # Kịch bản đặc biệt cho tai nghe
    script = {
        "product": "Premium Wireless Headphones - Model X1",
        "duration": 75,
        "model_description": "Nam chau A, da trang, mat den, toc den, 25 tuoi",
        "sections": {
            "hook": {
                "dialogue": "Ban co biet tai sao nhung nguoi thanh cong luon deo tai nghe cao cap khong?",
                "visual": "Close-up tai nghe tren tai nguoi mau nam chau A",
                "timing": "0-5s"
            },
            "introduction": {
                "dialogue": "Hom nay toi se review tai nghe Model X1 - san pham dang lam mua lam gio tren thi truong!",
                "visual": "Nguoi mau cam tai nghe, gioi thieu san pham",
                "timing": "5-15s"
            },
            "features": {
                "dialogue": "Diem noi bat: am thanh cuc ky trong treo voi cong nghe noise cancelling tien tien",
                "visual": "Nguoi mau deo tai nghe, bieu cam hai long",
                "timing": "15-30s"
            },
            "design": {
                "dialogue": "Thiet ke sang trong, deo ca ngay khong moi tai, pin 30 gio su dung lien tuc",
                "visual": "Close-up thiet ke tai nghe, nguoi mau trong tu the thoai mai",
                "timing": "30-45s"
            },
            "connectivity": {
                "dialogue": "Ket noi Bluetooth 5.0 sieu nhanh, tuong thich moi thiet bi, gia chi 2.5 trieu",
                "visual": "Nguoi mau ket noi voi dien thoai, su dung tai nghe",
                "timing": "45-60s"
            },
            "call_to_action": {
                "dialogue": "Dat hang ngay hom nay de duoc giam 20% va tang kem case bao ve cao cap!",
                "visual": "Nguoi mau chi tay ve phia camera, hien thi link mua hang",
                "timing": "60-75s"
            }
        }
    }
    
    # Tạo thư mục output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("outputs") / f"headphone_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Lưu cấu hình
    config_file = output_dir / "demo_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            "model_config": model_config,
            "keywords": keywords,
            "script": script,
            "output_dir": str(output_dir),
            "created_at": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cau hinh nguoi mau:")
    for key, value in model_config.items():
        print(f"   {key}: {value}")
    
    print(f"\n✅ Keywords: {', '.join(keywords)}")
    print(f"✅ San pham: {script['product']}")
    print(f"✅ Thoi luong: {script['duration']} giay")
    print(f"✅ Mo ta nguoi mau: {script['model_description']}")
    print(f"✅ Output directory: {output_dir}")
    print(f"✅ Config file: {config_file}")
    
    return output_dir, config_file

def create_model_prompts():
    """Tạo prompts cho người mẫu nam châu Á"""
    
    prompts = [
        "Asian male model, 25 years old, black hair, dark eyes, fair skin, wearing wireless headphones, professional studio photography, clean background, modern tech aesthetic, confident expression",
        "Young Asian man, black hair, dark eyes, light skin tone, wearing premium wireless earbuds, tech lifestyle photography, minimalist style, natural lighting",
        "Asian male, early 20s, black hair, dark eyes, wearing noise-cancelling headphones, casual pose, modern lifestyle, clean studio lighting, professional headshot",
        "Handsome Asian man, black hair, dark eyes, fair complexion, wearing high-end wireless headphones, studio portrait, tech product photography, commercial style"
    ]
    
    print(f"\n📝 Custom prompts cho nguoi mau nam chau A:")
    for i, prompt in enumerate(prompts, 1):
        print(f"   {i}. {prompt}")
    
    return prompts

def create_marketing_strategy():
    """Tạo chiến lược marketing cho tai nghe"""
    
    strategy = {
        "target_audience": "Nam 18-35 tuoi, quan tam den cong nghe, thu nhap trung binh tro len",
        "platforms": {
            "youtube": {
                "duration": "75 giay",
                "resolution": "1920x1080",
                "hashtags": ["#tai nghe", "#wireless", "#bluetooth", "#tech review", "#premium audio"],
                "posting_time": "20:00-22:00"
            },
            "tiktok": {
                "duration": "30 giay", 
                "resolution": "1080x1920",
                "hashtags": ["#tai nghe", "#wireless", "#tech", "#fyp", "#viral"],
                "posting_time": "18:00-21:00"
            },
            "instagram": {
                "duration": "60 giay",
                "resolution": "1080x1080", 
                "hashtags": ["#tai nghe", "#wireless", "#tech", "#lifestyle", "#premium"],
                "posting_time": "19:00-21:00"
            }
        },
        "budget_allocation": {
            "youtube_ads": 600,  # 40%
            "tiktok_ads": 450,   # 30%
            "instagram_ads": 300, # 20%
            "production": 150     # 10%
        },
        "success_metrics": {
            "views": 50000,
            "engagement_rate": 0.05,
            "conversion_rate": 0.02,
            "cost_per_acquisition": 50
        }
    }
    
    print(f"\n📊 Chien luoc marketing:")
    print(f"   Doi tuong muc tieu: {strategy['target_audience']}")
    print(f"   Ngan sach tong: {sum(strategy['budget_allocation'].values())} USD")
    print(f"   Muc tieu views: {strategy['success_metrics']['views']:,}")
    print(f"   Muc tieu engagement: {strategy['success_metrics']['engagement_rate']*100}%")
    
    return strategy

def main():
    """Main function"""
    
    print("DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A")
    print("=" * 50)
    
    # Tạo cấu hình demo
    output_dir, config_file = create_headphone_demo_config()
    
    # Tạo prompts
    prompts = create_model_prompts()
    
    # Tạo marketing strategy
    strategy = create_marketing_strategy()
    
    # Lưu tất cả vào file
    demo_data = {
        "config_file": str(config_file),
        "output_dir": str(output_dir),
        "model_prompts": prompts,
        "marketing_strategy": strategy,
        "created_at": datetime.now().isoformat()
    }
    
    demo_file = output_dir / "demo_summary.json"
    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 DEMO HOAN THANH!")
    print(f"📁 Thu muc ket qua: {output_dir}")
    print(f"📄 File cau hinh: {config_file}")
    print(f"📊 File tong hop: {demo_file}")
    
    print(f"\n📋 Cac buoc tiep theo:")
    print(f"   1. Cai dat dependencies: pip install -r requirements.txt")
    print(f"   2. Chay pipeline: python main.py --mode demo")
    print(f"   3. Kiem tra ket qua trong thu muc: {output_dir}")
    
    return output_dir

if __name__ == "__main__":
    main()
