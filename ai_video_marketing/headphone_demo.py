"""
Headphone Demo Script - No emoji version for Windows compatibility
"""
import sys
from pathlib import Path
import json
from datetime import datetime

def create_headphone_demo():
    """Tao demo cho tai nghe voi nguoi mau nam chau A"""
    
    print("DEMO: Tao video marketing cho tai nghe voi nguoi mau nam chau A")
    print("=" * 60)
    
    # Cau hinh nguoi mau nam chau A
    model_config = {
        "gender": "male",
        "age": "young adult",  # 20-30 tuoi
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
    
    # Kich ban dac biet cho tai nghe
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
    
    # Tao thu muc output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("outputs") / f"headphone_demo_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Luu cau hinh
    config_file = output_dir / "demo_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            "model_config": model_config,
            "keywords": keywords,
            "script": script,
            "output_dir": str(output_dir),
            "created_at": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print("Cau hinh nguoi mau:")
    for key, value in model_config.items():
        print(f"   {key}: {value}")
    
    print(f"\nKeywords: {', '.join(keywords)}")
    print(f"San pham: {script['product']}")
    print(f"Thoi luong: {script['duration']} giay")
    print(f"Mo ta nguoi mau: {script['model_description']}")
    print(f"Output directory: {output_dir}")
    print(f"Config file: {config_file}")
    
    return output_dir, config_file

def create_model_prompts():
    """Tao prompts cho nguoi mau nam chau A"""
    
    prompts = [
        "Asian male model, 25 years old, black hair, dark eyes, fair skin, wearing wireless headphones, professional studio photography, clean background, modern tech aesthetic, confident expression",
        "Young Asian man, black hair, dark eyes, light skin tone, wearing premium wireless earbuds, tech lifestyle photography, minimalist style, natural lighting",
        "Asian male, early 20s, black hair, dark eyes, wearing noise-cancelling headphones, casual pose, modern lifestyle, clean studio lighting, professional headshot",
        "Handsome Asian man, black hair, dark eyes, fair complexion, wearing high-end wireless headphones, studio portrait, tech product photography, commercial style"
    ]
    
    print(f"\nCustom prompts cho nguoi mau nam chau A:")
    for i, prompt in enumerate(prompts, 1):
        print(f"   {i}. {prompt}")
    
    return prompts

def create_marketing_strategy():
    """Tao chien luoc marketing cho tai nghe"""
    
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
    
    print(f"\nChien luoc marketing:")
    print(f"   Doi tuong muc tieu: {strategy['target_audience']}")
    print(f"   Ngan sach tong: {sum(strategy['budget_allocation'].values())} USD")
    print(f"   Muc tieu views: {strategy['success_metrics']['views']:,}")
    print(f"   Muc tieu engagement: {strategy['success_metrics']['engagement_rate']*100}%")
    
    return strategy

def create_ai_commands():
    """Tao cac lenh AI de chay pipeline"""
    
    commands = {
        "install_dependencies": "pip install torch torchvision transformers diffusers opencv-python moviepy",
        "run_demo": "python main.py --mode demo --keywords 'wireless headphones' 'bluetooth earbuds' --product 'Premium Wireless Headphones' --duration 75",
        "run_async": "python main.py --mode async --keywords 'wireless headphones' 'premium audio' --product 'Model X1 Headphones' --duration 60",
        "run_custom": "python main.py --mode custom --keywords 'noise cancelling' 'tech review' --product 'Premium Wireless Headphones' --duration 75 --output ./headphone_output"
    }
    
    print(f"\nCac lenh AI de chay:")
    for name, command in commands.items():
        print(f"   {name}: {command}")
    
    return commands

def main():
    """Main function"""
    
    print("DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A")
    print("=" * 50)
    
    # Tao cau hinh demo
    output_dir, config_file = create_headphone_demo()
    
    # Tao prompts
    prompts = create_model_prompts()
    
    # Tao marketing strategy
    strategy = create_marketing_strategy()
    
    # Tao AI commands
    commands = create_ai_commands()
    
    # Luu tat ca vao file
    demo_data = {
        "config_file": str(config_file),
        "output_dir": str(output_dir),
        "model_prompts": prompts,
        "marketing_strategy": strategy,
        "ai_commands": commands,
        "created_at": datetime.now().isoformat()
    }
    
    demo_file = output_dir / "demo_summary.json"
    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDEMO HOAN THANH!")
    print(f"Thu muc ket qua: {output_dir}")
    print(f"File cau hinh: {config_file}")
    print(f"File tong hop: {demo_file}")
    
    print(f"\nCac buoc tiep theo:")
    print(f"   1. Cai dat dependencies: pip install torch torchvision transformers diffusers")
    print(f"   2. Chay pipeline: python main.py --mode demo")
    print(f"   3. Kiem tra ket qua trong thu muc: {output_dir}")
    
    # Tao file batch script de chay
    batch_script = output_dir / "run_demo.bat"
    with open(batch_script, 'w', encoding='utf-8') as f:
        f.write("@echo off\n")
        f.write("echo Installing dependencies...\n")
        f.write("pip install torch torchvision transformers diffusers opencv-python moviepy\n")
        f.write("echo Running headphone demo...\n")
        f.write("python main.py --mode demo --keywords 'wireless headphones' 'bluetooth earbuds' --product 'Premium Wireless Headphones' --duration 75\n")
        f.write("pause\n")
    
    print(f"   4. Chay batch script: {batch_script}")
    
    return output_dir

if __name__ == "__main__":
    main()
