"""
Script Generator - Tạo kịch bản video dựa trên phân tích xu hướng
"""
import openai
import json
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
from datetime import datetime
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScriptGenerator:
    """Tạo kịch bản video marketing dựa trên xu hướng"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        openai.api_key = config.get("openai_api_key")
        
    def generate_video_script(self, 
                            trend_analysis: Dict[str, Any],
                            content_analysis: Dict[str, Any],
                            target_product: str = "",
                            video_duration: int = 60) -> Dict[str, Any]:
        """
        Tạo kịch bản video dựa trên phân tích xu hướng
        
        Args:
            trend_analysis: Kết quả phân tích xu hướng
            content_analysis: Kết quả phân tích nội dung
            target_product: Sản phẩm mục tiêu
            video_duration: Thời lượng video (giây)
            
        Returns:
            Dict[str, Any]: Kịch bản video hoàn chỉnh
        """
        logger.info("Generating video script based on trend analysis...")
        
        # Extract key insights
        insights = self._extract_key_insights(trend_analysis, content_analysis)
        
        # Generate script structure
        script_structure = self._generate_script_structure(insights, video_duration)
        
        # Generate detailed script
        detailed_script = self._generate_detailed_script(script_structure, insights, target_product)
        
        # Generate production notes
        production_notes = self._generate_production_notes(detailed_script, insights)
        
        # Generate marketing strategy
        marketing_strategy = self._generate_marketing_strategy(detailed_script, insights)
        
        script_result = {
            "script_info": {
                "generated_at": datetime.now().isoformat(),
                "video_duration": video_duration,
                "target_product": target_product,
                "based_on_trends": len(trend_analysis.get('videos', [])),
                "success_probability": insights.get('success_probability', 0)
            },
            "insights": insights,
            "script_structure": script_structure,
            "detailed_script": detailed_script,
            "production_notes": production_notes,
            "marketing_strategy": marketing_strategy
        }
        
        return script_result
    
    def _extract_key_insights(self, 
                            trend_analysis: Dict[str, Any],
                            content_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất insights quan trọng từ phân tích"""
        
        # Extract from trend analysis
        trending_factors = []
        common_tags = []
        optimal_duration = 60
        
        if 'analysis' in trend_analysis:
            analysis = trend_analysis['analysis']
            common_tags = list(analysis.get('common_tags', {}).keys())[:10]
            optimal_duration = analysis.get('duration_analysis', {}).get('optimal_duration', 60)
        
        # Extract from content analysis
        viral_elements = []
        engagement_patterns = []
        content_hooks = []
        
        if isinstance(content_analysis, list) and content_analysis:
            # Batch analysis results
            for analysis in content_analysis:
                if 'trend_analysis' in analysis:
                    trend_data = analysis['trend_analysis']
                    viral_elements.extend(trend_data.get('trending_factors', []))
                    content_hooks.extend(trend_data.get('content_hooks', []))
                
                if 'engagement_analysis' in analysis:
                    engagement_data = analysis['engagement_analysis']
                    engagement_patterns.append(engagement_data.get('engagement_level', 'average'))
        
        elif isinstance(content_analysis, dict):
            # Single analysis result
            if 'trend_analysis' in content_analysis:
                trend_data = content_analysis['trend_analysis']
                viral_elements.extend(trend_data.get('trending_factors', []))
                content_hooks.extend(trend_data.get('content_hooks', []))
            
            if 'engagement_analysis' in content_analysis:
                engagement_data = content_analysis['engagement_analysis']
                engagement_patterns.append(engagement_data.get('engagement_level', 'average'))
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(
            viral_elements, engagement_patterns, common_tags
        )
        
        return {
            "trending_factors": list(set(viral_elements)),
            "content_hooks": list(set(content_hooks)),
            "common_tags": common_tags,
            "optimal_duration": optimal_duration,
            "engagement_patterns": engagement_patterns,
            "success_probability": success_probability
        }
    
    def _calculate_success_probability(self, 
                                     viral_elements: List[str],
                                     engagement_patterns: List[str],
                                     common_tags: List[str]) -> float:
        """Tính toán xác suất thành công"""
        
        # Base score
        score = 5.0
        
        # Viral elements bonus
        score += min(len(viral_elements) * 0.5, 2.0)
        
        # Engagement patterns bonus
        excellent_count = engagement_patterns.count('excellent')
        good_count = engagement_patterns.count('good')
        score += excellent_count * 1.0 + good_count * 0.5
        
        # Tags relevance bonus
        score += min(len(common_tags) * 0.1, 1.0)
        
        return min(score, 10.0)
    
    def _generate_script_structure(self, 
                                 insights: Dict[str, Any],
                                 video_duration: int) -> Dict[str, Any]:
        """Tạo cấu trúc kịch bản"""
        
        # Calculate timing for each section
        hook_duration = min(5, video_duration * 0.1)  # 10% for hook
        intro_duration = min(10, video_duration * 0.15)  # 15% for intro
        main_duration = video_duration * 0.6  # 60% for main content
        cta_duration = min(10, video_duration * 0.15)  # 15% for CTA
        
        structure = {
            "hook": {
                "duration": hook_duration,
                "purpose": "Grab attention immediately",
                "elements": insights.get('content_hooks', [])[:2]
            },
            "introduction": {
                "duration": intro_duration,
                "purpose": "Introduce topic and build interest",
                "elements": ["Problem statement", "Solution preview"]
            },
            "main_content": {
                "duration": main_duration,
                "purpose": "Deliver value and build trust",
                "elements": insights.get('trending_factors', [])[:3]
            },
            "call_to_action": {
                "duration": cta_duration,
                "purpose": "Drive action",
                "elements": ["Clear instruction", "Urgency", "Benefit reminder"]
            }
        }
        
        return structure
    
    def _generate_detailed_script(self, 
                                script_structure: Dict[str, Any],
                                insights: Dict[str, Any],
                                target_product: str) -> Dict[str, Any]:
        """Tạo kịch bản chi tiết"""
        
        try:
            prompt = f"""
            Tạo kịch bản video marketing chi tiết dựa trên thông tin sau:
            
            Cấu trúc kịch bản:
            {json.dumps(script_structure, indent=2, ensure_ascii=False)}
            
            Insights từ xu hướng:
            - Yếu tố viral: {', '.join(insights.get('trending_factors', []))}
            - Content hooks: {', '.join(insights.get('content_hooks', []))}
            - Tags phổ biến: {', '.join(insights.get('common_tags', []))}
            - Thời lượng tối ưu: {insights.get('optimal_duration', 60)} giây
            
            Sản phẩm mục tiêu: {target_product or 'Sản phẩm tổng quát'}
            
            Hãy tạo kịch bản chi tiết với:
            1. Lời thoại chính xác cho từng phần
            2. Hướng dẫn visual cho từng cảnh
            3. Timing cụ thể
            4. Tone và style phù hợp
            
            Trả về JSON:
            {{
                "hook": {{
                    "dialogue": "Lời thoại hook",
                    "visual_notes": "Ghi chú visual",
                    "timing": "0-5s",
                    "tone": "exciting, curious"
                }},
                "introduction": {{
                    "dialogue": "Lời thoại intro",
                    "visual_notes": "Ghi chú visual",
                    "timing": "5-15s",
                    "tone": "informative, engaging"
                }},
                "main_content": {{
                    "sections": [
                        {{
                            "dialogue": "Lời thoại phần 1",
                            "visual_notes": "Ghi chú visual",
                            "timing": "15-45s",
                            "tone": "educational, convincing"
                        }}
                    ]
                }},
                "call_to_action": {{
                    "dialogue": "Lời thoại CTA",
                    "visual_notes": "Ghi chú visual",
                    "timing": "45-60s",
                    "tone": "urgent, compelling"
                }}
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia viết kịch bản video marketing. Tạo kịch bản hấp dẫn, có tính thuyết phục và phù hợp với xu hướng."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating detailed script: {e}")
            return {"error": str(e)}
    
    def _generate_production_notes(self, 
                                 detailed_script: Dict[str, Any],
                                 insights: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo ghi chú sản xuất"""
        
        try:
            prompt = f"""
            Dựa trên kịch bản video sau, hãy tạo ghi chú sản xuất chi tiết:
            
            Kịch bản:
            {json.dumps(detailed_script, indent=2, ensure_ascii=False)}
            
            Insights:
            {json.dumps(insights, indent=2, ensure_ascii=False)}
            
            Trả về JSON với các ghi chú:
            {{
                "equipment_needed": ["Thiết bị cần thiết"],
                "location_requirements": "Yêu cầu địa điểm",
                "lighting_setup": "Thiết lập ánh sáng",
                "audio_requirements": "Yêu cầu âm thanh",
                "visual_effects": ["Hiệu ứng visual"],
                "editing_notes": ["Ghi chú chỉnh sửa"],
                "color_grading": "Hướng dẫn color grading",
                "music_suggestions": ["Gợi ý nhạc nền"],
                "estimated_production_time": "Thời gian sản xuất ước tính",
                "budget_considerations": "Cân nhắc ngân sách"
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia sản xuất video. Đưa ra ghi chú chi tiết và thực tế."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating production notes: {e}")
            return {"error": str(e)}
    
    def _generate_marketing_strategy(self, 
                                   detailed_script: Dict[str, Any],
                                   insights: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo chiến lược marketing"""
        
        try:
            prompt = f"""
            Dựa trên kịch bản video, hãy tạo chiến lược marketing toàn diện:
            
            Kịch bản:
            {json.dumps(detailed_script, indent=2, ensure_ascii=False)}
            
            Insights:
            {json.dumps(insights, indent=2, ensure_ascii=False)}
            
            Trả về JSON:
            {{
                "target_audience": "Đối tượng mục tiêu chi tiết",
                "platform_strategy": {{
                    "youtube": "Chiến lược YouTube",
                    "tiktok": "Chiến lược TikTok",
                    "instagram": "Chiến lược Instagram",
                    "facebook": "Chiến lược Facebook"
                }},
                "posting_schedule": "Lịch đăng video",
                "hashtag_strategy": ["Hashtag 1", "Hashtag 2"],
                "engagement_tactics": ["Chiến thuật tương tác"],
                "conversion_optimization": "Tối ưu chuyển đổi",
                "budget_allocation": "Phân bổ ngân sách",
                "success_metrics": ["Chỉ số thành công"],
                "follow_up_content": ["Nội dung tiếp theo"]
            }}
            """
            
            response = openai.ChatCompletion.create(
                model=self.config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia marketing video. Tạo chiến lược toàn diện và thực tế."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating marketing strategy: {e}")
            return {"error": str(e)}
    
    def generate_multiple_scripts(self, 
                                trend_analysis: Dict[str, Any],
                                content_analysis: Dict[str, Any],
                                script_variations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Tạo nhiều biến thể kịch bản
        
        Args:
            trend_analysis: Phân tích xu hướng
            content_analysis: Phân tích nội dung
            script_variations: Danh sách biến thể kịch bản
            
        Returns:
            List[Dict[str, Any]]: Danh sách kịch bản
        """
        scripts = []
        
        for i, variation in enumerate(script_variations):
            logger.info(f"Generating script variation {i+1}/{len(script_variations)}")
            
            script = self.generate_video_script(
                trend_analysis=trend_analysis,
                content_analysis=content_analysis,
                target_product=variation.get('target_product', ''),
                video_duration=variation.get('duration', 60)
            )
            
            script['variation_info'] = variation
            scripts.append(script)
        
        return scripts
    
    def save_script(self, 
                   script: Dict[str, Any],
                   output_dir: Path,
                   filename: str = None) -> Path:
        """
        Lưu kịch bản vào file
        
        Args:
            script: Kịch bản
            output_dir: Thư mục lưu
            filename: Tên file
            
        Returns:
            Path: Đường dẫn file đã lưu
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_script_{timestamp}.json"
        
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Script saved to: {filepath}")
        return filepath

# Example usage
if __name__ == "__main__":
    from configs.config import AI_CONFIG, OUTPUTS_DIR
    
    # Initialize generator
    generator = ScriptGenerator(AI_CONFIG["openai"])
    
    # Sample data
    trend_analysis = {
        "videos": [],
        "analysis": {
            "common_tags": {"cooking": 15, "tips": 12, "food": 10},
            "duration_analysis": {"optimal_duration": 60}
        }
    }
    
    content_analysis = [{
        "trend_analysis": {
            "trending_factors": ["Quick tips", "Visual appeal", "Practical value"],
            "content_hooks": ["Problem-solution", "Before-after"]
        },
        "engagement_analysis": {
            "engagement_level": "good"
        }
    }]
    
    # Generate script
    script = generator.generate_video_script(
        trend_analysis=trend_analysis,
        content_analysis=content_analysis,
        target_product="Cooking Course",
        video_duration=60
    )
    
    # Save script
    output_dir = OUTPUTS_DIR / "scripts"
    generator.save_script(script, output_dir)
    
    print("Script generated successfully!")
    print(f"Script saved to: {output_dir}")

