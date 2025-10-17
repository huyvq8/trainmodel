"""
Demo script cho sản phẩm tai nghe với người mẫu nam châu Á
"""
import sys
from pathlib import Path
import asyncio
import json
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from main import AIVideoMarketingSystem
from configs.config import OUTPUTS_DIR

def create_headphone_demo():
    """Tạo demo cho sản phẩm tai nghe"""
    
    print("🎧 DEMO: Tạo video marketing cho tai nghe với người mẫu nam châu Á")
    print("=" * 70)
    
    # Khởi tạo hệ thống
    print("🚀 Khởi tạo hệ thống AI Video Marketing...")
    system = AIVideoMarketingSystem()
    
    # Cấu hình cho tai nghe
    keywords = [
        "wireless headphones",
        "bluetooth earbuds", 
        "noise cancelling",
        "premium audio",
        "tech review"
    ]
    
    target_product = "Premium Wireless Headphones - Model X1"
    video_duration = 75  # 75 giây
    
    # Tạo thư mục output riêng
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUTS_DIR / f"headphone_demo_{timestamp}"
    
    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Sản phẩm: {target_product}")
    print(f"⏱️ Thời lượng video: {video_duration} giây")
    print(f"🔍 Keywords: {', '.join(keywords)}")
    print()
    
    try:
        # Chạy pipeline đầy đủ
        print("🎬 Bắt đầu tạo video...")
        results = system.run_full_pipeline(
            keywords=keywords,
            target_product=target_product,
            video_duration=video_duration,
            output_dir=output_dir
        )
        
        # Hiển thị kết quả
        print("\n" + "="*70)
        print("🎉 HOÀN THÀNH! Kết quả:")
        print("="*70)
        
        if results.get("pipeline_info", {}).get("success"):
            print(f"✅ Pipeline thành công!")
            print(f"📁 Thư mục kết quả: {results['pipeline_info']['output_dir']}")
            
            # Hiển thị chi tiết từng bước
            steps = results.get("steps", {})
            
            if "trend_analysis" in steps:
                print(f"📊 Trend Analysis: {steps['trend_analysis']['videos_found']} video trending")
            
            if "model_generation" in steps:
                print(f"👤 Model Images: {steps['model_generation']['images_generated']} ảnh người mẫu")
            
            if "script_generation" in steps:
                success_rate = steps['script_generation'].get('success_probability', 0)
                print(f"📝 Script: Xác suất thành công {success_rate:.1f}/10")
            
            if "video_production" in steps:
                duration = steps['video_production'].get('duration', 0)
                print(f"🎬 Video: {duration:.1f} giây")
            
            if "short_clips" in steps:
                clips = steps['short_clips'].get('clips_created', 0)
                print(f"📱 Short Clips: {clips} clips")
            
            # Tạo marketing strategy cho tai nghe
            print("\n📊 Tạo chiến lược marketing...")
            main_video_path = output_dir / "main_video.mp4"
            if main_video_path.exists():
                marketing_result = system.generate_marketing_strategy(
                    video_path=str(main_video_path),
                    target_product=target_product,
                    budget=1500  # Budget cho tai nghe
                )
                print(f"✅ Marketing strategy: {marketing_result['strategy_file']}")
            
            print("\n🎯 Các file quan trọng:")
            print(f"   📹 Video chính: {output_dir}/main_video.mp4")
            print(f"   🎬 Video cuối: {output_dir}/final_video.mp4")
            print(f"   📱 Short clips: {output_dir}/short_clips/")
            print(f"   👤 Model images: {output_dir}/model_images/")
            print(f"   📝 Script: {output_dir}/scripts/")
            print(f"   📊 Analysis: {output_dir}/trend_analysis/")
            
        else:
            print("❌ Pipeline thất bại!")
            error = results.get("pipeline_info", {}).get("error", "Unknown error")
            print(f"Lỗi: {error}")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

def create_custom_model_config():
    """Tạo cấu hình người mẫu tùy chỉnh cho tai nghe"""
    
    print("\n👤 Tạo cấu hình người mẫu nam châu Á...")
    
    # Cấu hình người mẫu theo yêu cầu
    model_config = {
        "gender": "male",
        "age": "young adult",  # 20-30 tuổi
        "ethnicity": "asian",
        "style": "professional",
        "setting": "studio",
        "clothing": "casual smart"  # Phù hợp với tai nghe
    }
    
    # Prompt tùy chỉnh cho tai nghe
    custom_prompts = [
        "Asian male model, 25 years old, black hair, dark eyes, fair skin, wearing wireless headphones, professional studio photography, clean background, modern tech aesthetic",
        "Young Asian man, black hair, dark eyes, light skin tone, wearing premium wireless earbuds, confident expression, tech lifestyle photography, minimalist style",
        "Asian male, early 20s, black hair, dark eyes, wearing noise-cancelling headphones, casual pose, modern lifestyle, clean studio lighting"
    ]
    
    print("✅ Cấu hình người mẫu:")
    for key, value in model_config.items():
        print(f"   {key}: {value}")
    
    print("\n📝 Custom prompts:")
    for i, prompt in enumerate(custom_prompts, 1):
        print(f"   {i}. {prompt}")
    
    return model_config, custom_prompts

def create_headphone_specific_script():
    """Tạo kịch bản đặc biệt cho tai nghe"""
    
    print("\n📝 Tạo kịch bản đặc biệt cho tai nghe...")
    
    script_template = {
        "hook": {
            "dialogue": "Bạn có biết tại sao những người thành công luôn đeo tai nghe cao cấp không?",
            "visual_notes": "Close-up của tai nghe trên tai người mẫu nam châu Á",
            "timing": "0-5s",
            "tone": "curious, engaging"
        },
        "introduction": {
            "dialogue": "Hôm nay tôi sẽ review tai nghe Model X1 - sản phẩm đang làm mưa làm gió trên thị trường!",
            "visual_notes": "Người mẫu cầm tai nghe, giới thiệu sản phẩm",
            "timing": "5-15s",
            "tone": "excited, informative"
        },
        "main_content": {
            "sections": [
                {
                    "dialogue": "Điểm nổi bật đầu tiên: âm thanh cực kỳ trong trẻo với công nghệ noise cancelling tiên tiến",
                    "visual_notes": "Người mẫu đeo tai nghe, biểu cảm hài lòng",
                    "timing": "15-30s",
                    "tone": "impressed, technical"
                },
                {
                    "dialogue": "Thiết kế sang trọng, đeo cả ngày không mỏi tai, pin 30 giờ sử dụng liên tục",
                    "visual_notes": "Close-up thiết kế tai nghe, người mẫu trong tư thế thoải mái",
                    "timing": "30-45s",
                    "tone": "confident, detailed"
                },
                {
                    "dialogue": "Kết nối Bluetooth 5.0 siêu nhanh, tương thích mọi thiết bị, giá chỉ 2.5 triệu",
                    "visual_notes": "Người mẫu kết nối với điện thoại, sử dụng tai nghe",
                    "timing": "45-60s",
                    "tone": "persuasive, value-focused"
                }
            ]
        },
        "call_to_action": {
            "dialogue": "Đặt hàng ngay hôm nay để được giảm 20% và tặng kèm case bảo vệ cao cấp! Link mua hàng ở mô tả!",
            "visual_notes": "Người mẫu chỉ tay về phía camera, hiển thị link mua hàng",
            "timing": "60-75s",
            "tone": "urgent, compelling"
        }
    }
    
    print("✅ Kịch bản tai nghe:")
    for section, content in script_template.items():
        if isinstance(content, dict) and "dialogue" in content:
            print(f"   {section}: {content['dialogue']}")
        elif isinstance(content, dict) and "sections" in content:
            for i, sub_section in enumerate(content["sections"]):
                print(f"   {section} {i+1}: {sub_section['dialogue']}")
    
    return script_template

async def run_async_headphone_demo():
    """Chạy demo async cho tai nghe"""
    
    print("\n⚡ Chạy demo async (nhanh hơn 2-3 lần)...")
    
    system = AIVideoMarketingSystem()
    
    keywords = ["wireless headphones", "bluetooth earbuds", "premium audio"]
    target_product = "Premium Wireless Headphones - Model X1"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUTS_DIR / f"headphone_async_{timestamp}"
    
    try:
        results = await system.run_async_pipeline(
            keywords=keywords,
            target_product=target_product,
            video_duration=60,
            output_dir=output_dir
        )
        
        print("✅ Async pipeline hoàn thành!")
        print(f"📁 Kết quả: {output_dir}")
        
    except Exception as e:
        print(f"❌ Lỗi async: {e}")

if __name__ == "__main__":
    print("🎧 DEMO TAI NGHE VỚI NGƯỜI MẪU NAM CHÂU Á")
    print("=" * 50)
    
    # Tạo cấu hình người mẫu
    model_config, custom_prompts = create_custom_model_config()
    
    # Tạo kịch bản tai nghe
    script_template = create_headphone_specific_script()
    
    # Chạy demo chính
    create_headphone_demo()
    
    # Chạy demo async (tùy chọn)
    print("\n" + "="*50)
    choice = input("Bạn có muốn chạy demo async (nhanh hơn)? (y/n): ")
    if choice.lower() == 'y':
        asyncio.run(run_async_headphone_demo())
    
    print("\n🎉 Demo hoàn thành!")
    print("📁 Kiểm tra thư mục outputs/ để xem kết quả")
