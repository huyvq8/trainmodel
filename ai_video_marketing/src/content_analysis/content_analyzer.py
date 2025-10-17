"""
Content Analyzer - Phân tích nội dung video với ChatGPT
"""
import openai
import json
import requests
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
from datetime import datetime
import base64
import cv2
import numpy as np
from PIL import Image
import io

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentAnalyzer:
    """Phân tích nội dung video với AI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        openai.api_key = config.get("openai_api_key")
        
    def analyze_video_content(self, 
                            video_data: Dict[str, Any],
                            extract_frames: bool = True) -> Dict[str, Any]:
        """
        Phân tích nội dung video toàn diện
        
        Args:
            video_data: Thông tin video
            extract_frames: Có trích xuất frames không
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        logger.info(f"Analyzing video: {video_data.get('title', 'Unknown')}")
        
        analysis = {
            'video_info': video_data,
            'text_analysis': {},
            'visual_analysis': {},
            'engagement_analysis': {},
            'trend_analysis': {},
            'recommendations': {}
        }
        
        # 1. Phân tích text (title, description, comments)
        analysis['text_analysis'] = self._analyze_text_content(video_data)
        
        # 2. Phân tích visual (nếu có frames)
        if extract_frames and video_data.get('url'):
            analysis['visual_analysis'] = self._analyze_visual_content(video_data)
        
        # 3. Phân tích engagement
        analysis['engagement_analysis'] = self._analyze_engagement(video_data)
        
        # 4. Phân tích xu hướng
        analysis['trend_analysis'] = self._analyze_trend_factors(video_data)
        
        # 5. Đưa ra khuyến nghị
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_text_content(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích nội dung text"""
        try:
            # Combine title, description, and tags
            text_content = f"""
            Title: {video_data.get('title', '')}
            Description: {video_data.get('description', '')}
            Tags: {', '.join(video_data.get('tags', []))}
            """
            
            prompt = f"""
            Phân tích nội dung video sau và trả về kết quả dưới dạng JSON:
            
            {text_content}
            
            Hãy phân tích và trả về JSON với các trường:
            {{
                "main_topic": "Chủ đề chính của video",
                "target_audience": "Đối tượng mục tiêu",
                "content_type": "Loại nội dung (educational, entertainment, promotional, etc.)",
                "key_messages": ["Thông điệp chính 1", "Thông điệp chính 2"],
                "emotional_tone": "Tone cảm xúc (positive, negative, neutral, exciting, etc.)",
                "call_to_action": "Lời kêu gọi hành động (nếu có)",
                "keywords": ["từ khóa quan trọng 1", "từ khóa quan trọng 2"],
                "content_quality_score": 8.5,
                "viral_potential": 7.2,
                "marketing_value": 6.8
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia phân tích nội dung video marketing. Hãy phân tích chi tiết và chính xác."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get("max_tokens", 2000),
                temperature=self.config.get("temperature", 0.7)
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing text content: {e}")
            return {"error": str(e)}
    
    def _analyze_visual_content(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích nội dung visual"""
        try:
            # Extract frames from video (mock implementation)
            frames = self._extract_video_frames(video_data.get('url', ''))
            
            if not frames:
                return {"error": "Could not extract frames"}
            
            # Analyze frames with GPT-4 Vision
            visual_analysis = []
            
            for i, frame in enumerate(frames[:5]):  # Analyze first 5 frames
                analysis = self._analyze_frame_with_gpt4v(frame, i)
                visual_analysis.append(analysis)
            
            return {
                "frame_analysis": visual_analysis,
                "visual_consistency": self._analyze_visual_consistency(visual_analysis),
                "color_scheme": self._analyze_color_scheme(frames),
                "composition_quality": self._analyze_composition(frames)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing visual content: {e}")
            return {"error": str(e)}
    
    def _extract_video_frames(self, video_url: str) -> List[np.ndarray]:
        """Trích xuất frames từ video"""
        try:
            # Mock implementation - in real scenario, you'd download and process video
            # For now, return empty list
            logger.info(f"Extracting frames from: {video_url}")
            return []
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return []
    
    def _analyze_frame_with_gpt4v(self, frame: np.ndarray, frame_index: int) -> Dict[str, Any]:
        """Phân tích frame với GPT-4 Vision"""
        try:
            # Convert frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            prompt = f"""
            Phân tích frame {frame_index} của video và trả về JSON:
            {{
                "main_subjects": ["Đối tượng chính trong frame"],
                "scene_type": "Loại cảnh (indoor, outdoor, studio, etc.)",
                "lighting": "Chất lượng ánh sáng (good, poor, dramatic, etc.)",
                "composition": "Bố cục (balanced, dynamic, static, etc.)",
                "emotions": ["Cảm xúc thể hiện"],
                "brand_elements": ["Yếu tố thương hiệu (nếu có)"],
                "visual_quality": 8.5
            }}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{frame_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error analyzing frame with GPT-4V: {e}")
            return {"error": str(e)}
    
    def _analyze_visual_consistency(self, frame_analyses: List[Dict]) -> Dict[str, Any]:
        """Phân tích tính nhất quán visual"""
        if not frame_analyses:
            return {}
        
        # Analyze consistency across frames
        scene_types = [analysis.get('scene_type', '') for analysis in frame_analyses]
        lighting_quality = [analysis.get('lighting', '') for analysis in frame_analyses]
        
        return {
            "scene_consistency": len(set(scene_types)) == 1,
            "lighting_consistency": len(set(lighting_quality)) <= 2,
            "overall_consistency_score": 8.0  # Mock score
        }
    
    def _analyze_color_scheme(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Phân tích color scheme"""
        if not frames:
            return {}
        
        # Mock color analysis
        return {
            "dominant_colors": ["#FF5733", "#33FF57", "#3357FF"],
            "color_harmony": "complementary",
            "brightness": "medium",
            "saturation": "high"
        }
    
    def _analyze_composition(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Phân tích bố cục"""
        if not frames:
            return {}
        
        return {
            "rule_of_thirds": True,
            "symmetry": False,
            "depth_of_field": "shallow",
            "composition_score": 7.5
        }
    
    def _analyze_engagement(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích engagement metrics"""
        views = video_data.get('views', 0)
        likes = video_data.get('likes', 0)
        comments = video_data.get('comments', 0)
        
        if views == 0:
            return {"error": "No view data available"}
        
        engagement_rate = (likes + comments) / views
        
        return {
            "engagement_rate": engagement_rate,
            "like_rate": likes / views,
            "comment_rate": comments / views,
            "engagement_level": self._classify_engagement_level(engagement_rate),
            "viral_potential": self._calculate_viral_potential(video_data)
        }
    
    def _classify_engagement_level(self, engagement_rate: float) -> str:
        """Phân loại mức độ engagement"""
        if engagement_rate > 0.1:
            return "excellent"
        elif engagement_rate > 0.05:
            return "good"
        elif engagement_rate > 0.02:
            return "average"
        else:
            return "poor"
    
    def _calculate_viral_potential(self, video_data: Dict[str, Any]) -> float:
        """Tính toán tiềm năng viral"""
        views = video_data.get('views', 0)
        likes = video_data.get('likes', 0)
        comments = video_data.get('comments', 0)
        duration = video_data.get('duration', 0)
        
        # Simple viral potential calculation
        engagement_score = (likes + comments * 2) / max(views, 1)
        duration_score = 1 / (1 + duration / 60)  # Shorter videos tend to be more viral
        view_score = min(views / 1000000, 1)  # Normalize to 1M views
        
        viral_potential = (engagement_score * 0.4 + duration_score * 0.3 + view_score * 0.3) * 10
        
        return min(viral_potential, 10.0)
    
    def _analyze_trend_factors(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích các yếu tố xu hướng"""
        try:
            prompt = f"""
            Phân tích các yếu tố làm video này trở nên trending và trả về JSON:
            
            Title: {video_data.get('title', '')}
            Description: {video_data.get('description', '')}
            Views: {video_data.get('views', 0)}
            Likes: {video_data.get('likes', 0)}
            Comments: {video_data.get('comments', 0)}
            Duration: {video_data.get('duration', 0)} seconds
            Tags: {', '.join(video_data.get('tags', []))}
            
            Trả về JSON:
            {{
                "trending_factors": ["Yếu tố 1", "Yếu tố 2", "Yếu tố 3"],
                "content_hooks": ["Hook 1", "Hook 2"],
                "emotional_triggers": ["Cảm xúc 1", "Cảm xúc 2"],
                "shareability_factors": ["Yếu tố chia sẻ 1", "Yếu tố chia sẻ 2"],
                "timing_factors": "Yếu tố thời gian",
                "trend_score": 8.5
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia phân tích xu hướng video marketing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error analyzing trend factors: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo khuyến nghị dựa trên phân tích"""
        try:
            # Combine all analysis results
            combined_analysis = {
                "text": analysis.get('text_analysis', {}),
                "visual": analysis.get('visual_analysis', {}),
                "engagement": analysis.get('engagement_analysis', {}),
                "trend": analysis.get('trend_analysis', {})
            }
            
            prompt = f"""
            Dựa trên phân tích video sau, hãy đưa ra khuyến nghị để tạo video tương tự thành công:
            
            {json.dumps(combined_analysis, indent=2, ensure_ascii=False)}
            
            Trả về JSON với các khuyến nghị:
            {{
                "content_recommendations": ["Khuyến nghị nội dung 1", "Khuyến nghị nội dung 2"],
                "visual_recommendations": ["Khuyến nghị visual 1", "Khuyến nghị visual 2"],
                "engagement_recommendations": ["Khuyến nghị engagement 1", "Khuyến nghị engagement 2"],
                "script_suggestions": ["Gợi ý kịch bản 1", "Gợi ý kịch bản 2"],
                "production_tips": ["Mẹo sản xuất 1", "Mẹo sản xuất 2"],
                "marketing_strategy": "Chiến lược marketing",
                "success_probability": 8.2
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tư vấn video marketing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {"error": str(e)}
    
    def batch_analyze_videos(self, 
                           videos: List[Dict[str, Any]],
                           output_dir: Path) -> List[Dict[str, Any]]:
        """
        Phân tích hàng loạt video
        
        Args:
            videos: Danh sách video
            output_dir: Thư mục lưu kết quả
            
        Returns:
            List[Dict[str, Any]]: Kết quả phân tích
        """
        results = []
        
        for i, video in enumerate(videos):
            logger.info(f"Analyzing video {i+1}/{len(videos)}: {video.get('title', 'Unknown')}")
            
            try:
                analysis = self.analyze_video_content(video)
                results.append(analysis)
                
                # Save individual analysis
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analysis_{i+1:03d}_{timestamp}.json"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                
            except Exception as e:
                logger.error(f"Error analyzing video {i+1}: {e}")
                results.append({"error": str(e), "video": video})
        
        # Save batch results
        batch_file = output_dir / f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Batch analysis completed. Results saved to: {output_dir}")
        return results

# Example usage
if __name__ == "__main__":
    from configs.config import AI_CONFIG, OUTPUTS_DIR
    
    # Initialize analyzer
    analyzer = ContentAnalyzer(AI_CONFIG["openai"])
    
    # Sample video data
    sample_video = {
        "title": "Amazing Cooking Tips That Will Change Your Life",
        "description": "Learn these incredible cooking techniques that professional chefs use every day!",
        "views": 150000,
        "likes": 8500,
        "comments": 420,
        "duration": 120,
        "tags": ["cooking", "tips", "chef", "food", "tutorial"]
    }
    
    # Analyze video
    analysis = analyzer.analyze_video_content(sample_video)
    
    # Save results
    output_dir = OUTPUTS_DIR / "content_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"analysis_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis completed and saved to: {output_file}")

