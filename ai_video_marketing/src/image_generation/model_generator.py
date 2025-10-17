"""
AI Model Generator - Tạo ảnh người mẫu chân thực với Stable Diffusion
"""
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import numpy as np
from pathlib import Path
import logging
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelGenerator:
    """Tạo ảnh người mẫu chân thực với AI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None
        self._load_model()
        
    def _load_model(self):
        """Load Stable Diffusion model"""
        try:
            logger.info(f"Loading Stable Diffusion model on {self.device}...")
            
            # Load pipeline
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.config["model_id"],
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Set scheduler
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory efficient attention
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                self.pipe.enable_vae_slicing()
                
            logger.info("Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate_model_photo(self, 
                           prompt: str, 
                           negative_prompt: str = "",
                           num_images: int = 1,
                           seed: Optional[int] = None) -> List[Image.Image]:
        """
        Tạo ảnh người mẫu từ prompt
        
        Args:
            prompt: Mô tả người mẫu muốn tạo
            negative_prompt: Những gì không muốn trong ảnh
            num_images: Số lượng ảnh tạo
            seed: Random seed để tái tạo kết quả
            
        Returns:
            List[Image.Image]: Danh sách ảnh được tạo
        """
        try:
            # Set seed if provided
            if seed is not None:
                torch.manual_seed(seed)
                if torch.cuda.is_available():
                    torch.cuda.manual_seed(seed)
            
            # Default negative prompt for realistic human photos
            if not negative_prompt:
                negative_prompt = (
                    "blurry, low quality, distorted, deformed, ugly, "
                    "cartoon, anime, painting, sketch, drawing, "
                    "multiple people, crowd, group, "
                    "nude, nsfw, inappropriate, "
                    "text, watermark, signature"
                )
            
            # Generate images
            logger.info(f"Generating {num_images} model photos...")
            logger.info(f"Prompt: {prompt}")
            
            images = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_images_per_prompt=num_images,
                num_inference_steps=self.config["num_inference_steps"],
                guidance_scale=self.config["guidance_scale"],
                width=self.config["width"],
                height=self.config["height"]
            ).images
            
            logger.info(f"Generated {len(images)} images successfully!")
            return images
            
        except Exception as e:
            logger.error(f"Error generating images: {e}")
            raise
    
    def create_model_prompts(self, 
                           gender: str = "female",
                           age: str = "young adult",
                           ethnicity: str = "asian",
                           style: str = "professional",
                           setting: str = "studio",
                           clothing: str = "business casual") -> str:
        """
        Tạo prompt tối ưu cho người mẫu
        
        Args:
            gender: Giới tính (male/female)
            age: Độ tuổi (teen, young adult, middle aged, senior)
            ethnicity: Dân tộc (asian, caucasian, african, hispanic, mixed)
            style: Phong cách (professional, casual, elegant, trendy)
            setting: Bối cảnh (studio, outdoor, office, home)
            clothing: Trang phục (business casual, formal, casual, sporty)
            
        Returns:
            str: Prompt được tối ưu hóa
        """
        
        # Base prompt for realistic human
        base_prompt = (
            "professional photography, high quality, detailed, "
            "realistic, photorealistic, 8k resolution, "
            "sharp focus, perfect lighting, studio lighting, "
            "beautiful, attractive, confident, natural expression"
        )
        
        # Gender and age
        person_desc = f"{age} {gender}"
        
        # Ethnicity
        if ethnicity == "asian":
            person_desc += ", asian features, vietnamese, southeast asian"
        elif ethnicity == "caucasian":
            person_desc += ", caucasian features, european"
        elif ethnicity == "african":
            person_desc += ", african features, black"
        elif ethnicity == "hispanic":
            person_desc += ", hispanic features, latino"
        elif ethnicity == "mixed":
            person_desc += ", mixed ethnicity, diverse features"
        
        # Style and setting
        style_desc = f"{style} {setting} photography"
        
        # Clothing
        clothing_desc = f"wearing {clothing}"
        
        # Combine all elements
        full_prompt = f"{person_desc}, {clothing_desc}, {style_desc}, {base_prompt}"
        
        return full_prompt
    
    def generate_model_variations(self, 
                                base_prompt: str,
                                variations: List[Dict[str, str]]) -> Dict[str, List[Image.Image]]:
        """
        Tạo nhiều biến thể của người mẫu
        
        Args:
            base_prompt: Prompt cơ bản
            variations: List các biến thể (clothing, pose, expression, etc.)
            
        Returns:
            Dict[str, List[Image.Image]]: Kết quả theo từng biến thể
        """
        results = {}
        
        for i, variation in enumerate(variations):
            logger.info(f"Generating variation {i+1}/{len(variations)}: {variation}")
            
            # Create variation prompt
            variation_prompt = f"{base_prompt}, {variation.get('description', '')}"
            
            # Generate images for this variation
            images = self.generate_model_photo(
                prompt=variation_prompt,
                num_images=variation.get('num_images', 1),
                seed=variation.get('seed')
            )
            
            results[variation.get('name', f'variation_{i+1}')] = images
        
        return results
    
    def save_images(self, 
                   images: List[Image.Image], 
                   output_dir: Path,
                   prefix: str = "model",
                   format: str = "PNG") -> List[Path]:
        """
        Lưu ảnh vào thư mục
        
        Args:
            images: Danh sách ảnh
            output_dir: Thư mục lưu
            prefix: Tiền tố tên file
            format: Định dạng ảnh
            
        Returns:
            List[Path]: Đường dẫn các file đã lưu
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_paths = []
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, image in enumerate(images):
            filename = f"{prefix}_{timestamp}_{i+1:03d}.{format.lower()}"
            filepath = output_dir / filename
            
            # Save image
            image.save(filepath, format=format, quality=95)
            saved_paths.append(filepath)
            
            logger.info(f"Saved image: {filepath}")
        
        return saved_paths
    
    def create_model_portfolio(self, 
                             model_config: Dict[str, Any],
                             output_dir: Path) -> Dict[str, Any]:
        """
        Tạo portfolio hoàn chỉnh cho người mẫu
        
        Args:
            model_config: Cấu hình người mẫu
            output_dir: Thư mục lưu kết quả
            
        Returns:
            Dict[str, Any]: Thông tin portfolio
        """
        logger.info("Creating model portfolio...")
        
        # Create base prompt
        base_prompt = self.create_model_prompts(**model_config)
        
        # Define variations
        variations = [
            {
                "name": "professional_headshot",
                "description": "professional headshot, business attire, confident smile, clean background",
                "num_images": 3
            },
            {
                "name": "casual_portrait",
                "description": "casual portrait, relaxed pose, natural lighting, friendly expression",
                "num_images": 3
            },
            {
                "name": "lifestyle_shot",
                "description": "lifestyle photography, natural setting, candid moment, authentic expression",
                "num_images": 2
            }
        ]
        
        # Generate variations
        portfolio_images = self.generate_model_variations(base_prompt, variations)
        
        # Save all images
        portfolio_info = {
            "model_config": model_config,
            "base_prompt": base_prompt,
            "generated_at": datetime.now().isoformat(),
            "images": {}
        }
        
        for variation_name, images in portfolio_images.items():
            variation_dir = output_dir / variation_name
            saved_paths = self.save_images(images, variation_dir, variation_name)
            portfolio_info["images"][variation_name] = [str(p) for p in saved_paths]
        
        # Save portfolio metadata
        metadata_path = output_dir / "portfolio_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(portfolio_info, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Portfolio created successfully in {output_dir}")
        return portfolio_info

# Example usage
if __name__ == "__main__":
    from configs.config import AI_CONFIG, OUTPUTS_DIR
    
    # Initialize generator
    generator = ModelGenerator(AI_CONFIG["stable_diffusion"])
    
    # Create model portfolio
    model_config = {
        "gender": "female",
        "age": "young adult", 
        "ethnicity": "asian",
        "style": "professional",
        "setting": "studio",
        "clothing": "business casual"
    }
    
    output_dir = OUTPUTS_DIR / "model_portfolio"
    portfolio = generator.create_model_portfolio(model_config, output_dir)
    
    print("Model portfolio created successfully!")
    print(f"Images saved in: {output_dir}")

