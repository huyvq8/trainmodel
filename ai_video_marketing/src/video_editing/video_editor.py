"""
Video Editor - Lắp ghép và chỉnh sửa video thành phẩm
"""
import moviepy.editor as mp
from moviepy.video.fx import resize, speedx, fadein, fadeout
from moviepy.audio.fx import volumex
import cv2
import numpy as np
from PIL import Image
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoEditor:
    """Chỉnh sửa và lắp ghép video thành phẩm"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def create_final_video(self, 
                         video_clips: List[str],
                         script: Dict[str, Any],
                         output_path: Path) -> Dict[str, Any]:
        """
        Tạo video cuối cùng từ các clip
        
        Args:
            video_clips: Danh sách đường dẫn video clips
            script: Kịch bản video
            output_path: Đường dẫn lưu video cuối
            
        Returns:
            Dict[str, Any]: Thông tin video cuối
        """
        logger.info("Creating final video from clips...")
        
        # Load video clips
        clips = []
        for clip_path in video_clips:
            if Path(clip_path).exists():
                clip = mp.VideoFileClip(clip_path)
                clips.append(clip)
            else:
                logger.warning(f"Clip not found: {clip_path}")
        
        if not clips:
            raise ValueError("No valid video clips found")
        
        # Apply transitions between clips
        clips_with_transitions = self._add_transitions(clips)
        
        # Combine all clips
        final_video = mp.concatenate_videoclips(clips_with_transitions, method="compose")
        
        # Apply final effects
        final_video = self._apply_final_effects(final_video)
        
        # Add intro/outro
        final_video = self._add_intro_outro(final_video, script)
        
        # Optimize for different platforms
        optimized_videos = self._optimize_for_platforms(final_video, output_path)
        
        # Clean up
        for clip in clips:
            clip.close()
        final_video.close()
        
        return {
            "output_paths": optimized_videos,
            "total_duration": sum(clip.duration for clip in clips),
            "clips_count": len(clips),
            "created_at": datetime.now().isoformat()
        }
    
    def _add_transitions(self, clips: List[mp.VideoFileClip]) -> List[mp.VideoFileClip]:
        """Thêm transition giữa các clip"""
        if len(clips) <= 1:
            return clips
        
        clips_with_transitions = []
        
        for i, clip in enumerate(clips):
            # Add fade in for first clip
            if i == 0:
                clip = clip.fadein(0.5)
            
            # Add fade out for last clip
            if i == len(clips) - 1:
                clip = clip.fadeout(0.5)
            
            # Add crossfade for middle clips
            else:
                clip = clip.fadeout(0.3)
            
            clips_with_transitions.append(clip)
        
        return clips_with_transitions
    
    def _apply_final_effects(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Áp dụng hiệu ứng cuối cùng"""
        try:
            # Ensure consistent resolution
            target_resolution = self.config.get('default_resolution', (1920, 1080))
            video = video.resize(target_resolution)
            
            # Apply color correction
            video = self._apply_color_correction(video)
            
            # Apply sharpening
            video = self._apply_sharpening(video)
            
            # Add subtle vignette
            video = self._add_vignette(video)
            
            return video
            
        except Exception as e:
            logger.error(f"Error applying final effects: {e}")
            return video
    
    def _apply_color_correction(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Áp dụng color correction"""
        try:
            # This is a simplified color correction
            # In a real implementation, you'd use more sophisticated color grading
            
            def color_correct(get_frame, t):
                frame = get_frame(t)
                # Convert to float for processing
                frame = frame.astype(np.float32) / 255.0
                
                # Increase contrast slightly
                frame = np.clip((frame - 0.5) * 1.1 + 0.5, 0, 1)
                
                # Increase saturation slightly
                hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                hsv[:, :, 1] = hsv[:, :, 1] * 1.1
                frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
                
                # Convert back to uint8
                return (frame * 255).astype(np.uint8)
            
            return video.fl(color_correct)
            
        except Exception as e:
            logger.error(f"Error applying color correction: {e}")
            return video
    
    def _apply_sharpening(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Áp dụng sharpening"""
        try:
            def sharpen(get_frame, t):
                frame = get_frame(t)
                
                # Create sharpening kernel
                kernel = np.array([[-1,-1,-1],
                                 [-1, 9,-1],
                                 [-1,-1,-1]])
                
                # Apply sharpening
                sharpened = cv2.filter2D(frame, -1, kernel)
                
                # Blend with original (50% sharpened, 50% original)
                return cv2.addWeighted(frame, 0.5, sharpened, 0.5, 0)
            
            return video.fl(sharpen)
            
        except Exception as e:
            logger.error(f"Error applying sharpening: {e}")
            return video
    
    def _add_vignette(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Thêm vignette effect"""
        try:
            def add_vignette(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                
                # Create vignette mask
                y, x = np.ogrid[:h, :w]
                center_x, center_y = w // 2, h // 2
                
                # Calculate distance from center
                mask = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                mask = mask / mask.max()
                
                # Apply vignette (subtle effect)
                vignette_strength = 0.3
                vignette = 1 - mask * vignette_strength
                
                # Apply to each color channel
                for i in range(3):
                    frame[:, :, i] = frame[:, :, i] * vignette
                
                return frame.astype(np.uint8)
            
            return video.fl(add_vignette)
            
        except Exception as e:
            logger.error(f"Error adding vignette: {e}")
            return video
    
    def _add_intro_outro(self, 
                        video: mp.VideoFileClip,
                        script: Dict[str, Any]) -> mp.VideoFileClip:
        """Thêm intro và outro"""
        try:
            # Create intro clip
            intro_clip = self._create_intro_clip(script)
            
            # Create outro clip
            outro_clip = self._create_outro_clip(script)
            
            # Combine intro + main video + outro
            if intro_clip and outro_clip:
                final_video = mp.concatenate_videoclips([intro_clip, video, outro_clip])
                intro_clip.close()
                outro_clip.close()
                return final_video
            elif intro_clip:
                final_video = mp.concatenate_videoclips([intro_clip, video])
                intro_clip.close()
                return final_video
            elif outro_clip:
                final_video = mp.concatenate_videoclips([video, outro_clip])
                outro_clip.close()
                return final_video
            else:
                return video
                
        except Exception as e:
            logger.error(f"Error adding intro/outro: {e}")
            return video
    
    def _create_intro_clip(self, script: Dict[str, Any]) -> Optional[mp.VideoFileClip]:
        """Tạo intro clip"""
        try:
            # Get brand info from script
            brand_name = script.get('script_info', {}).get('target_product', 'Our Brand')
            
            # Create intro text
            intro_text = f"Welcome to {brand_name}"
            
            # Create text clip
            intro_clip = mp.TextClip(
                intro_text,
                fontsize=60,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold'
            ).set_duration(3)
            
            # Add background
            intro_clip = intro_clip.on_color(
                size=(1920, 1080),
                color=(0, 0, 0),
                pos='center'
            )
            
            # Add fade effects
            intro_clip = intro_clip.fadein(0.5).fadeout(0.5)
            
            return intro_clip
            
        except Exception as e:
            logger.error(f"Error creating intro clip: {e}")
            return None
    
    def _create_outro_clip(self, script: Dict[str, Any]) -> Optional[mp.VideoFileClip]:
        """Tạo outro clip"""
        try:
            # Create outro text
            outro_text = "Thank you for watching!\nDon't forget to like and subscribe!"
            
            # Create text clip
            outro_clip = mp.TextClip(
                outro_text,
                fontsize=50,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold',
                method='caption',
                size=(1800, None)
            ).set_duration(5)
            
            # Add background
            outro_clip = outro_clip.on_color(
                size=(1920, 1080),
                color=(0, 0, 0),
                pos='center'
            )
            
            # Add fade effects
            outro_clip = outro_clip.fadein(0.5).fadeout(0.5)
            
            return outro_clip
            
        except Exception as e:
            logger.error(f"Error creating outro clip: {e}")
            return None
    
    def _optimize_for_platforms(self, 
                              video: mp.VideoFileClip,
                              base_output_path: Path) -> Dict[str, str]:
        """Tối ưu video cho các platform khác nhau"""
        optimized_videos = {}
        
        # YouTube (1080p)
        youtube_path = base_output_path.parent / f"{base_output_path.stem}_youtube.mp4"
        youtube_video = video.resize((1920, 1080))
        youtube_video.write_videofile(
            str(youtube_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k'
        )
        optimized_videos['youtube'] = str(youtube_path)
        youtube_video.close()
        
        # TikTok (9:16 aspect ratio)
        tiktok_path = base_output_path.parent / f"{base_output_path.stem}_tiktok.mp4"
        tiktok_video = video.resize((1080, 1920))
        tiktok_video.write_videofile(
            str(tiktok_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            bitrate='3000k'
        )
        optimized_videos['tiktok'] = str(tiktok_path)
        tiktok_video.close()
        
        # Instagram (1:1 aspect ratio)
        instagram_path = base_output_path.parent / f"{base_output_path.stem}_instagram.mp4"
        instagram_video = video.resize((1080, 1080))
        instagram_video.write_videofile(
            str(instagram_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            bitrate='4000k'
        )
        optimized_videos['instagram'] = str(instagram_path)
        instagram_video.close()
        
        return optimized_videos
    
    def create_short_clips(self, 
                         main_video_path: str,
                         script: Dict[str, Any],
                         output_dir: Path) -> List[Dict[str, Any]]:
        """
        Tạo các clip ngắn từ video chính
        
        Args:
            main_video_path: Đường dẫn video chính
            script: Kịch bản
            output_dir: Thư mục lưu clips
            
        Returns:
            List[Dict[str, Any]]: Thông tin các clip ngắn
        """
        logger.info("Creating short clips from main video...")
        
        if not Path(main_video_path).exists():
            raise FileNotFoundError(f"Main video not found: {main_video_path}")
        
        # Load main video
        main_video = mp.VideoFileClip(main_video_path)
        
        # Extract key moments based on script
        key_moments = self._extract_key_moments(script, main_video.duration)
        
        short_clips = []
        
        for i, moment in enumerate(key_moments):
            # Create short clip
            start_time = moment['start']
            end_time = moment['end']
            
            short_clip = main_video.subclip(start_time, end_time)
            
            # Add branding
            short_clip = self._add_branding(short_clip, moment['title'])
            
            # Save clip
            clip_path = output_dir / f"short_clip_{i+1:03d}.mp4"
            short_clip.write_videofile(
                str(clip_path),
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )
            
            short_clips.append({
                'path': str(clip_path),
                'title': moment['title'],
                'duration': end_time - start_time,
                'start_time': start_time,
                'end_time': end_time
            })
            
            short_clip.close()
        
        main_video.close()
        
        return short_clips
    
    def _extract_key_moments(self, 
                           script: Dict[str, Any],
                           total_duration: float) -> List[Dict[str, Any]]:
        """Trích xuất các khoảnh khắc quan trọng"""
        key_moments = []
        
        # Extract from script sections
        detailed_script = script.get('detailed_script', {})
        
        current_time = 0
        
        # Hook moment
        if 'hook' in detailed_script:
            hook_duration = self._parse_timing(detailed_script['hook'].get('timing', '0-5s'))
            key_moments.append({
                'title': 'Hook - Attention Grabber',
                'start': current_time,
                'end': current_time + hook_duration
            })
            current_time += hook_duration
        
        # Main content highlights
        if 'main_content' in detailed_script:
            sections = detailed_script['main_content'].get('sections', [])
            for i, section in enumerate(sections[:3]):  # Take first 3 sections
                section_duration = self._parse_timing(section.get('timing', '10s'))
                key_moments.append({
                    'title': f'Key Point {i+1}',
                    'start': current_time,
                    'end': current_time + section_duration
                })
                current_time += section_duration
        
        # CTA moment
        if 'call_to_action' in detailed_script:
            cta_duration = self._parse_timing(detailed_script['call_to_action'].get('timing', '5s'))
            key_moments.append({
                'title': 'Call to Action',
                'start': max(0, total_duration - cta_duration),
                'end': total_duration
            })
        
        return key_moments
    
    def _parse_timing(self, timing_str: str) -> float:
        """Parse timing string to duration"""
        try:
            import re
            numbers = re.findall(r'\d+', timing_str)
            if len(numbers) >= 2:
                return float(numbers[1]) - float(numbers[0])
            elif len(numbers) == 1:
                return float(numbers[0])
            else:
                return 10.0
        except:
            return 10.0
    
    def _add_branding(self, clip: mp.VideoFileClip, title: str) -> mp.VideoFileClip:
        """Thêm branding cho clip"""
        try:
            # Create title overlay
            title_clip = mp.TextClip(
                title,
                fontsize=40,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold'
            ).set_duration(clip.duration)
            
            # Position at top
            title_clip = title_clip.set_position(('center', 'top')).set_margin(20)
            
            # Add logo (if available)
            logo_clip = None
            logo_path = Path("data/logo.png")
            if logo_path.exists():
                logo_clip = mp.ImageClip(str(logo_path)).set_duration(clip.duration)
                logo_clip = logo_clip.resize(height=60).set_position(('left', 'top')).set_margin(20)
            
            # Combine clips
            if logo_clip:
                return mp.CompositeVideoClip([clip, title_clip, logo_clip])
            else:
                return mp.CompositeVideoClip([clip, title_clip])
                
        except Exception as e:
            logger.error(f"Error adding branding: {e}")
            return clip
    
    def batch_edit_videos(self, 
                         video_paths: List[str],
                         scripts: List[Dict[str, Any]],
                         output_dir: Path) -> List[Dict[str, Any]]:
        """
        Chỉnh sửa hàng loạt video
        
        Args:
            video_paths: Danh sách đường dẫn video
            scripts: Danh sách kịch bản
            output_dir: Thư mục lưu
            
        Returns:
            List[Dict[str, Any]]: Thông tin video đã chỉnh sửa
        """
        results = []
        
        for i, (video_path, script) in enumerate(zip(video_paths, scripts)):
            logger.info(f"Editing video {i+1}/{len(video_paths)}")
            
            try:
                # Create output path
                output_path = output_dir / f"edited_video_{i+1:03d}.mp4"
                
                # Edit video
                result = self.create_final_video([video_path], script, output_path)
                result['original_path'] = video_path
                result['script_index'] = i
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error editing video {i+1}: {e}")
                results.append({
                    'error': str(e),
                    'original_path': video_path,
                    'script_index': i
                })
        
        return results

# Example usage
if __name__ == "__main__":
    from configs.config import VIDEO_CONFIG, OUTPUTS_DIR
    
    # Initialize editor
    editor = VideoEditor(VIDEO_CONFIG)
    
    # Sample video clips
    video_clips = [
        "outputs/video_clip_1.mp4",
        "outputs/video_clip_2.mp4",
        "outputs/video_clip_3.mp4"
    ]
    
    # Sample script
    sample_script = {
        "script_info": {
            "target_product": "Cooking Course"
        },
        "detailed_script": {
            "hook": {"timing": "0-5s"},
            "main_content": {
                "sections": [
                    {"timing": "5-25s"},
                    {"timing": "25-45s"}
                ]
            },
            "call_to_action": {"timing": "45-60s"}
        }
    }
    
    # Create final video
    output_path = OUTPUTS_DIR / "final_video.mp4"
    result = editor.create_final_video(video_clips, sample_script, output_path)
    
    print(f"Final video created: {result}")

