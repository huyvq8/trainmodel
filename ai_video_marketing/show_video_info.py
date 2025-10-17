"""
Show Video Information for Headphone Demo
"""
import json
from pathlib import Path

def show_video_info():
    """Hien thi thong tin video demo"""
    
    print("THONG TIN VIDEO DEMO TAI NGHE")
    print("=" * 40)
    
    # Doc cau hinh demo
    config_file = Path("outputs/headphone_demo_20251017_214847/demo_config.json")
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("CAU HINH NGUOI MAU:")
        model_config = config["model_config"]
        print(f"   Gioi tinh: {model_config['gender']}")
        print(f"   Do tuoi: {model_config['age']}")
        print(f"   Dan toc: {model_config['ethnicity']}")
        print(f"   Phong cach: {model_config['style']}")
        print(f"   Boi canh: {model_config['setting']}")
        print(f"   Trang phuc: {model_config['clothing']}")
        
        print(f"\nSAN PHAM:")
        print(f"   Ten: {config['script']['product']}")
        print(f"   Thoi luong: {config['script']['duration']} giay")
        print(f"   Mo ta nguoi mau: {config['script']['model_description']}")
        
        print(f"\nKEYWORDS:")
        for i, keyword in enumerate(config['keywords'], 1):
            print(f"   {i}. {keyword}")
        
        print(f"\nKICH BAN VIDEO (6 PHAN):")
        sections = config['script']['sections']
        for name, section in sections.items():
            print(f"   {name.upper()}:")
            print(f"      Thoi gian: {section['timing']}")
            print(f"      Loi thoai: {section['dialogue']}")
            print(f"      Visual: {section['visual']}")
            print()
        
        print("TOI UU CHO CAC PLATFORM:")
        print("   YouTube: 1920x1080, 75s, hashtags: #tai nghe #wireless #bluetooth #tech review")
        print("   TikTok: 1080x1920, 30s, hashtags: #tai nghe #wireless #tech #fyp")
        print("   Instagram: 1080x1080, 60s, hashtags: #tai nghe #wireless #tech #lifestyle")
        
        print(f"\nMUC TIEU:")
        print("   Views: 50,000+")
        print("   Engagement rate: 5%+")
        print("   Conversion rate: 2%+")
        
    else:
        print("Khong tim thay file cau hinh demo!")
        return False
    
    return True

def show_ai_prompts():
    """Hien thi AI prompts cho nguoi mau"""
    
    print("\nAI PROMPTS CHO NGUOI MAU NAM CHAU A:")
    print("=" * 45)
    
    prompts = [
        "Asian male model, 25 years old, black hair, dark eyes, fair skin, wearing wireless headphones, professional studio photography, clean background, modern tech aesthetic, confident expression",
        "Young Asian man, black hair, dark eyes, light skin tone, wearing premium wireless earbuds, tech lifestyle photography, minimalist style, natural lighting",
        "Asian male, early 20s, black hair, dark eyes, wearing noise-cancelling headphones, casual pose, modern lifestyle, clean studio lighting, professional headshot",
        "Handsome Asian man, black hair, dark eyes, fair complexion, wearing high-end wireless headphones, studio portrait, tech product photography, commercial style"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt}")
        print()

def show_commands():
    """Hien thi cac lenh de chay"""
    
    print("CAC LENH DE TAO VIDEO:")
    print("=" * 25)
    
    print("1. Cai dat dependencies:")
    print("   pip install torch torchvision transformers diffusers opencv-python moviepy")
    print()
    
    print("2. Chay demo:")
    print("   python main.py --mode demo --keywords 'wireless headphones' 'bluetooth earbuds' --product 'Premium Wireless Headphones' --duration 75")
    print()
    
    print("3. Chay async (nhanh hon):")
    print("   python main.py --mode async --keywords 'wireless headphones' 'premium audio' --product 'Model X1 Headphones' --duration 60")
    print()
    
    print("4. Chay custom:")
    print("   python main.py --mode custom --keywords 'noise cancelling' 'tech review' --product 'Premium Wireless Headphones' --duration 75 --output ./headphone_output")
    print()

def show_expected_results():
    """Hien thi ket qua mong doi"""
    
    print("KET QUA MONG DOI:")
    print("=" * 20)
    
    print("FILES SE DUOC TAO:")
    print("   - main_video.mp4 (video chinh 75 giay)")
    print("   - final_video_youtube.mp4 (toi uu cho YouTube)")
    print("   - final_video_tiktok.mp4 (toi uu cho TikTok)")
    print("   - final_video_instagram.mp4 (toi uu cho Instagram)")
    print("   - model_images/ (anh nguoi mau AI)")
    print("   - short_clips/ (clips ngan cho social media)")
    print("   - scripts/ (kich ban chi tiet)")
    print("   - trend_analysis/ (phan tich xu huong)")
    print()
    
    print("THOI GIAN XU LY:")
    print("   - Demo mode: 10-15 phut")
    print("   - Async mode: 5-8 phut")
    print("   - Custom mode: 8-12 phut")
    print()

def main():
    """Main function"""
    
    print("DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A")
    print("=" * 45)
    
    # Hien thi thong tin video
    if show_video_info():
        print("Da doc thong tin video thanh cong!")
    
    # Hien thi AI prompts
    show_ai_prompts()
    
    # Hien thi cac lenh
    show_commands()
    
    # Hien thi ket qua mong doi
    show_expected_results()
    
    print("DE XEM VIDEO THUC TE:")
    print("1. Cai dat dependencies")
    print("2. Chay pipeline AI")
    print("3. Kiem tra thu muc outputs/")
    print()
    print("Hoac chay: python run_headphone_demo.py")

if __name__ == "__main__":
    main()
