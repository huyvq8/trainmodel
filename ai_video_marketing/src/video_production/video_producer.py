"""
Video Producer - Sản xuất video với AI
"""
import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
from moviepy.video.fx import resize, speedx
from moviepy.audio.fx import volumex
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime
import textwrap
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProducer:
    """Sản xuất video với AI và các công cụ local"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def create_video_from_script(self, 
                               script: Dict[str, Any],
                               model_images: List[Image.Image],
                               output_path: Path) -> Dict[str, Any]:
        """
        Tạo video từ kịch bản và ảnh người mẫu
        
        Args:
            script: Kịch bản video
            model_images: Ảnh người mẫu
            output_path: Đường dẫn lưu video
            
        Returns:
            Dict[str, Any]: Thông tin video đã tạo
        """
        logger.info("Creating video from script...")
        
        # Extract script sections
        script_sections = script.get('detailed_script', {})
        
        # Create video clips for each section
        video_clips = []
        total_duration = 0
        
        # Hook section
        if 'hook' in script_sections:
            hook_clip = self._create_section_clip(
                script_sections['hook'],
                model_images,
                section_type='hook'
            )
            if hook_clip:
                video_clips.append(hook_clip)
                total_duration += hook_clip.duration
        
        # Introduction section
        if 'introduction' in script_sections:
            intro_clip = self._create_section_clip(
                script_sections['introduction'],
                model_images,
                section_type='introduction'
            )
            if intro_clip:
                video_clips.append(intro_clip)
                total_duration += intro_clip.duration
        
        # Main content sections
        if 'main_content' in script_sections:
            main_sections = script_sections['main_content'].get('sections', [])
            for section in main_sections:
                main_clip = self._create_section_clip(
                    section,
                    model_images,
                    section_type='main'
                )
                if main_clip:
                    video_clips.append(main_clip)
                    total_duration += main_clip.duration
        
        # Call to action section
        if 'call_to_action' in script_sections:
            cta_clip = self._create_section_clip(
                script_sections['call_to_action'],
                model_images,
                section_type='cta'
            )
            if cta_clip:
                video_clips.append(cta_clip)
                total_duration += cta_clip.duration
        
        if not video_clips:
            raise ValueError("No video clips created")
        
        # Combine all clips
        final_video = mp.concatenate_videoclips(video_clips, method="compose")
        
        # Add background music
        final_video = self._add_background_music(final_video)
        
        # Apply final effects
        final_video = self._apply_final_effects(final_video)
        
        # Export video
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_video.write_videofile(
            str(output_path),
            fps=self.config.get('fps', 30),
            codec=self.config.get('codec', 'libx264'),
            audio_codec=self.config.get('audio_codec', 'aac'),
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        for clip in video_clips:
            clip.close()
        final_video.close()
        
        video_info = {
            "output_path": str(output_path),
            "duration": total_duration,
            "resolution": self.config.get('default_resolution', (1920, 1080)),
            "fps": self.config.get('fps', 30),
            "sections_count": len(video_clips),
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"Video created successfully: {output_path}")
        return video_info
    
    def _create_section_clip(self, 
                           section: Dict[str, Any],
                           model_images: List[Image.Image],
                           section_type: str) -> Optional[mp.VideoFileClip]:
        """Tạo clip cho một section"""
        try:
            dialogue = section.get('dialogue', '')
            visual_notes = section.get('visual_notes', '')
            timing = section.get('timing', '0-10s')
            tone = section.get('tone', 'neutral')
            
            # Parse timing
            duration = self._parse_timing(timing)
            
            # Select appropriate model image
            model_image = self._select_model_image(model_images, section_type)
            
            # Create visual content
            visual_clip = self._create_visual_content(
                model_image, dialogue, visual_notes, duration, tone
            )
            
            # Add text overlay
            text_clip = self._create_text_overlay(dialogue, duration, tone)
            
            # Combine visual and text
            if text_clip:
                final_clip = mp.CompositeVideoClip([visual_clip, text_clip])
            else:
                final_clip = visual_clip
            
            return final_clip
            
        except Exception as e:
            logger.error(f"Error creating section clip: {e}")
            return None
    
    def _parse_timing(self, timing_str: str) -> float:
        """Parse timing string to duration in seconds"""
        try:
            # Extract numbers from timing string like "0-10s" or "15-45s"
            import re
            numbers = re.findall(r'\d+', timing_str)
            if len(numbers) >= 2:
                return float(numbers[1]) - float(numbers[0])
            elif len(numbers) == 1:
                return float(numbers[0])
            else:
                return 10.0  # Default duration
        except:
            return 10.0
    
    def _select_model_image(self, 
                          model_images: List[Image.Image],
                          section_type: str) -> Image.Image:
        """Chọn ảnh người mẫu phù hợp cho section"""
        if not model_images:
            # Create a placeholder image
            return self._create_placeholder_image()
        
        # Select image based on section type
        if section_type == 'hook':
            return model_images[0]  # Use first image for hook
        elif section_type == 'cta':
            return model_images[-1]  # Use last image for CTA
        else:
            # Randomly select for other sections
            return random.choice(model_images)
    
    def _create_placeholder_image(self) -> Image.Image:
        """Tạo ảnh placeholder"""
        img = Image.new('RGB', (1920, 1080), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = "AI Generated Content"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        return img
    
    def _create_visual_content(self, 
                             model_image: Image.Image,
                             dialogue: str,
                             visual_notes: str,
                             duration: float,
                             tone: str) -> mp.VideoFileClip:
        """Tạo nội dung visual cho clip"""
        
        # Resize model image to video resolution
        target_resolution = self.config.get('default_resolution', (1920, 1080))
        model_image = model_image.resize(target_resolution, Image.Resampling.LANCZOS)
        
        # Apply visual effects based on tone
        if tone in ['exciting', 'urgent']:
            # Add dynamic effects
            model_image = self._apply_dynamic_effects(model_image)
        elif tone in ['calm', 'peaceful']:
            # Add calming effects
            model_image = self._apply_calming_effects(model_image)
        
        # Convert PIL image to numpy array
        img_array = np.array(model_image)
        
        # Create video clip from image
        clip = mp.ImageClip(img_array, duration=duration)
        
        # Add subtle zoom effect
        clip = clip.resize(lambda t: 1 + 0.1 * t / duration)
        
        return clip
    
    def _apply_dynamic_effects(self, image: Image.Image) -> Image.Image:
        """Áp dụng hiệu ứng động"""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Increase saturation slightly
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        hsv[:, :, 1] = hsv[:, :, 1] * 1.2  # Increase saturation
        img_array = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        # Convert back to PIL
        return Image.fromarray(img_array)
    
    def _apply_calming_effects(self, image: Image.Image) -> Image.Image:
        """Áp dụng hiệu ứng êm dịu"""
        # Convert to numpy array
        img_array = np.array(image)
        
        # Slight blur for calming effect
        img_array = cv2.GaussianBlur(img_array, (5, 5), 0)
        
        # Convert back to PIL
        return Image.fromarray(img_array)
    
    def _create_text_overlay(self, 
                           dialogue: str,
                           duration: float,
                           tone: str) -> Optional[mp.TextClip]:
        """Tạo text overlay cho clip"""
        if not dialogue.strip():
            return None
        
        try:
            # Configure text style based on tone
            font_size = 50
            color = 'white'
            stroke_color = 'black'
            stroke_width = 2
            
            if tone in ['exciting', 'urgent']:
                font_size = 60
                color = 'yellow'
                stroke_color = 'red'
                stroke_width = 3
            elif tone in ['calm', 'peaceful']:
                font_size = 45
                color = 'lightblue'
                stroke_color = 'darkblue'
                stroke_width = 1
            
            # Wrap text for better readability
            max_chars_per_line = 40
            wrapped_text = textwrap.fill(dialogue, width=max_chars_per_line)
            
            # Create text clip
            text_clip = mp.TextClip(
                wrapped_text,
                fontsize=font_size,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                font='Arial-Bold',
                method='caption',
                size=(1800, None)  # Leave some margin
            ).set_duration(duration)
            
            # Position text at bottom
            text_clip = text_clip.set_position(('center', 'bottom')).set_margin(50)
            
            return text_clip
            
        except Exception as e:
            logger.error(f"Error creating text overlay: {e}")
            return None
    
    def _add_background_music(self, video_clip: mp.VideoFileClip) -> mp.VideoFileClip:
        """Thêm nhạc nền"""
        try:
            # Look for background music file
            music_path = Path("data/background_music.mp3")
            
            if music_path.exists():
                # Load background music
                music = mp.AudioFileClip(str(music_path))
                
                # Adjust music duration to match video
                if music.duration > video_clip.duration:
                    music = music.subclip(0, video_clip.duration)
                else:
                    # Loop music if it's shorter than video
                    loops_needed = int(video_clip.duration / music.duration) + 1
                    music = mp.concatenate_audioclips([music] * loops_needed)
                    music = music.subclip(0, video_clip.duration)
                
                # Lower volume of background music
                music = music.fx(volumex, 0.3)
                
                # Combine with video audio (if any)
                if video_clip.audio:
                    final_audio = mp.CompositeAudioClip([video_clip.audio, music])
                else:
                    final_audio = music
                
                return video_clip.set_audio(final_audio)
            else:
                logger.warning("Background music file not found, skipping music")
                return video_clip
                
        except Exception as e:
            logger.error(f"Error adding background music: {e}")
            return video_clip
    
    def _apply_final_effects(self, video_clip: mp.VideoFileClip) -> mp.VideoFileClip:
        """Áp dụng hiệu ứng cuối cùng"""
        try:
            # Apply color correction
            video_clip = video_clip.fx(resize, newsize=self.config.get('default_resolution', (1920, 1080)))
            
            # Add subtle fade in/out
            video_clip = video_clip.fadein(0.5).fadeout(0.5)
            
            return video_clip
            
        except Exception as e:
            logger.error(f"Error applying final effects: {e}")
            return video_clip
    
    def create_multiple_variations(self, 
                                 script: Dict[str, Any],
                                 model_images: List[Image.Image],
                                 variations: List[Dict[str, Any]],
                                 output_dir: Path) -> List[Dict[str, Any]]:
        """
        Tạo nhiều biến thể video
        
        Args:
            script: Kịch bản gốc
            model_images: Ảnh người mẫu
            variations: Danh sách biến thể
            output_dir: Thư mục lưu
            
        Returns:
            List[Dict[str, Any]]: Thông tin các video đã tạo
        """
        results = []
        
        for i, variation in enumerate(variations):
            logger.info(f"Creating video variation {i+1}/{len(variations)}")
            
            # Modify script for this variation
            modified_script = self._modify_script_for_variation(script, variation)
            
            # Create output path
            output_path = output_dir / f"video_variation_{i+1:03d}.mp4"
            
            # Create video
            video_info = self.create_video_from_script(
                modified_script, model_images, output_path
            )
            
            video_info['variation'] = variation
            results.append(video_info)
        
        return results
    
    def _modify_script_for_variation(self, 
                                   script: Dict[str, Any],
                                   variation: Dict[str, Any]) -> Dict[str, Any]:
        """Chỉnh sửa kịch bản cho biến thể"""
        modified_script = script.copy()
        
        # Modify based on variation parameters
        if 'tone' in variation:
            # Update tone throughout script
            detailed_script = modified_script.get('detailed_script', {})
            for section in detailed_script.values():
                if isinstance(section, dict) and 'tone' in section:
                    section['tone'] = variation['tone']
        
        if 'duration' in variation:
            # Adjust timing
            target_duration = variation['duration']
            current_duration = script.get('script_info', {}).get('video_duration', 60)
            
            if target_duration != current_duration:
                # Scale all timings proportionally
                scale_factor = target_duration / current_duration
                # This would require more complex timing adjustment logic
                pass
        
        return modified_script
    
    def batch_produce_videos(self, 
                           scripts: List[Dict[str, Any]],
                           model_images: List[Image.Image],
                           output_dir: Path) -> List[Dict[str, Any]]:
        """
        Sản xuất hàng loạt video
        
        Args:
            scripts: Danh sách kịch bản
            model_images: Ảnh người mẫu
            output_dir: Thư mục lưu
            
        Returns:
            List[Dict[str, Any]]: Thông tin các video đã tạo
        """
        results = []
        
        for i, script in enumerate(scripts):
            logger.info(f"Producing video {i+1}/{len(scripts)}")
            
            # Create output path
            output_path = output_dir / f"video_{i+1:03d}.mp4"
            
            # Create video
            video_info = self.create_video_from_script(
                script, model_images, output_path
            )
            
            video_info['script_index'] = i
            results.append(video_info)
        
        return results

# Example usage
if __name__ == "__main__":
    from configs.config import VIDEO_CONFIG, OUTPUTS_DIR
    
    # Initialize producer
    producer = VideoProducer(VIDEO_CONFIG)
    
    # Sample script
    sample_script = {
        "detailed_script": {
            "hook": {
                "dialogue": "Bạn có biết bí mật này không?",
                "visual_notes": "Close-up of model with surprised expression",
                "timing": "0-5s",
                "tone": "exciting"
            },
            "introduction": {
                "dialogue": "Hôm nay tôi sẽ chia sẻ với bạn những mẹo hay nhất!",
                "visual_notes": "Model smiling and gesturing",
                "timing": "5-15s",
                "tone": "engaging"
            }
        }
    }
    
    # Sample model images (placeholder)
    model_images = []
    
    # Create video
    output_path = OUTPUTS_DIR / "sample_video.mp4"
    video_info = producer.create_video_from_script(sample_script, model_images, output_path)
    
    print(f"Video created: {video_info}")

