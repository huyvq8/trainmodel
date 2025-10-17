"""
Marketing Optimizer - Tối ưu hóa video cho marketing và bán hàng
"""
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timedelta
import re
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MarketingMetrics:
    """Metrics cho marketing"""
    engagement_rate: float
    conversion_rate: float
    click_through_rate: float
    cost_per_acquisition: float
    return_on_investment: float

@dataclass
class PlatformOptimization:
    """Tối ưu hóa cho từng platform"""
    platform: str
    optimal_duration: int
    optimal_resolution: tuple
    best_posting_times: List[str]
    recommended_hashtags: List[str]
    engagement_tactics: List[str]

class MarketingOptimizer:
    """Tối ưu hóa video cho marketing và bán hàng"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.platform_optimizations = self._initialize_platform_optimizations()
        
    def _initialize_platform_optimizations(self) -> Dict[str, PlatformOptimization]:
        """Khởi tạo tối ưu hóa cho từng platform"""
        return {
            "youtube": PlatformOptimization(
                platform="youtube",
                optimal_duration=120,  # 2 minutes
                optimal_resolution=(1920, 1080),
                best_posting_times=["14:00", "20:00", "22:00"],
                recommended_hashtags=["#trending", "#viral", "#subscribe", "#like"],
                engagement_tactics=[
                    "Ask viewers to subscribe in first 15 seconds",
                    "Use end screens to promote other videos",
                    "Pin important comments",
                    "Respond to comments quickly"
                ]
            ),
            "tiktok": PlatformOptimization(
                platform="tiktok",
                optimal_duration=30,  # 30 seconds
                optimal_resolution=(1080, 1920),
                best_posting_times=["18:00", "19:00", "20:00", "21:00"],
                recommended_hashtags=["#fyp", "#viral", "#trending", "#foryou"],
                engagement_tactics=[
                    "Hook viewers in first 3 seconds",
                    "Use trending sounds and effects",
                    "Post consistently at optimal times",
                    "Engage with comments immediately"
                ]
            ),
            "instagram": PlatformOptimization(
                platform="instagram",
                optimal_duration=60,  # 1 minute
                optimal_resolution=(1080, 1080),
                best_posting_times=["11:00", "14:00", "17:00", "19:00"],
                recommended_hashtags=["#instagood", "#viral", "#trending", "#reels"],
                engagement_tactics=[
                    "Use Instagram Stories for behind-the-scenes",
                    "Post Reels consistently",
                    "Use location tags",
                    "Collaborate with influencers"
                ]
            ),
            "facebook": PlatformOptimization(
                platform="facebook",
                optimal_duration=90,  # 1.5 minutes
                optimal_resolution=(1280, 720),
                best_posting_times=["13:00", "15:00", "18:00", "21:00"],
                recommended_hashtags=["#viral", "#trending", "#share"],
                engagement_tactics=[
                    "Use Facebook Live for real-time engagement",
                    "Create Facebook Groups for community",
                    "Use Facebook Ads for promotion",
                    "Share to relevant Facebook Pages"
                ]
            )
        }
    
    def optimize_video_for_platform(self, 
                                  video_path: str,
                                  platform: str,
                                  target_audience: str = "general") -> Dict[str, Any]:
        """
        Tối ưu hóa video cho platform cụ thể
        
        Args:
            video_path: Đường dẫn video
            platform: Platform mục tiêu
            target_audience: Đối tượng mục tiêu
            
        Returns:
            Dict[str, Any]: Kết quả tối ưu hóa
        """
        logger.info(f"Optimizing video for {platform}...")
        
        if platform not in self.platform_optimizations:
            raise ValueError(f"Unsupported platform: {platform}")
        
        platform_config = self.platform_optimizations[platform]
        
        # Analyze current video
        video_analysis = self._analyze_video(video_path)
        
        # Generate optimization recommendations
        recommendations = self._generate_optimization_recommendations(
            video_analysis, platform_config, target_audience
        )
        
        # Create optimized version
        optimized_video_path = self._create_optimized_video(
            video_path, platform_config, recommendations
        )
        
        return {
            "original_video": video_path,
            "optimized_video": optimized_video_path,
            "platform": platform,
            "recommendations": recommendations,
            "optimization_score": self._calculate_optimization_score(
                video_analysis, platform_config
            )
        }
    
    def _analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Phân tích video hiện tại"""
        try:
            import cv2
            
            cap = cv2.VideoCapture(video_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "duration": duration,
                "resolution": (width, height),
                "fps": fps,
                "aspect_ratio": width / height if height > 0 else 1,
                "file_size": Path(video_path).stat().st_size if Path(video_path).exists() else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return {
                "duration": 0,
                "resolution": (0, 0),
                "fps": 0,
                "aspect_ratio": 1,
                "file_size": 0
            }
    
    def _generate_optimization_recommendations(self,
                                             video_analysis: Dict[str, Any],
                                             platform_config: PlatformOptimization,
                                             target_audience: str) -> Dict[str, Any]:
        """Tạo khuyến nghị tối ưu hóa"""
        recommendations = {
            "duration_optimization": {},
            "resolution_optimization": {},
            "content_optimization": {},
            "engagement_optimization": {},
            "posting_optimization": {}
        }
        
        # Duration optimization
        current_duration = video_analysis["duration"]
        optimal_duration = platform_config.optimal_duration
        
        if abs(current_duration - optimal_duration) > 10:  # More than 10 seconds difference
            recommendations["duration_optimization"] = {
                "current": current_duration,
                "optimal": optimal_duration,
                "action": "trim" if current_duration > optimal_duration else "extend",
                "priority": "high"
            }
        
        # Resolution optimization
        current_resolution = video_analysis["resolution"]
        optimal_resolution = platform_config.optimal_resolution
        
        if current_resolution != optimal_resolution:
            recommendations["resolution_optimization"] = {
                "current": current_resolution,
                "optimal": optimal_resolution,
                "action": "resize",
                "priority": "high"
            }
        
        # Content optimization
        recommendations["content_optimization"] = {
            "hashtags": platform_config.recommended_hashtags,
            "engagement_tactics": platform_config.engagement_tactics,
            "target_audience": target_audience
        }
        
        # Engagement optimization
        recommendations["engagement_optimization"] = {
            "best_posting_times": platform_config.best_posting_times,
            "engagement_tactics": platform_config.engagement_tactics
        }
        
        # Posting optimization
        recommendations["posting_optimization"] = {
            "optimal_times": platform_config.best_posting_times,
            "frequency": "daily" if platform_config.platform == "tiktok" else "3-4 times per week"
        }
        
        return recommendations
    
    def _create_optimized_video(self,
                              video_path: str,
                              platform_config: PlatformOptimization,
                              recommendations: Dict[str, Any]) -> str:
        """Tạo video đã tối ưu hóa"""
        try:
            import moviepy.editor as mp
            
            # Load video
            video = mp.VideoFileClip(video_path)
            
            # Apply optimizations
            optimized_video = video
            
            # Duration optimization
            if recommendations["duration_optimization"]:
                duration_rec = recommendations["duration_optimization"]
                if duration_rec["action"] == "trim":
                    optimized_video = optimized_video.subclip(0, duration_rec["optimal"])
                elif duration_rec["action"] == "extend":
                    # Extend by looping or adding content
                    loops_needed = int(duration_rec["optimal"] / video.duration) + 1
                    optimized_video = mp.concatenate_videoclips([video] * loops_needed)
                    optimized_video = optimized_video.subclip(0, duration_rec["optimal"])
            
            # Resolution optimization
            if recommendations["resolution_optimization"]:
                resolution_rec = recommendations["resolution_optimization"]
                optimized_video = optimized_video.resize(resolution_rec["optimal"])
            
            # Save optimized video
            output_path = Path(video_path).parent / f"optimized_{platform_config.platform}_{Path(video_path).name}"
            optimized_video.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            video.close()
            optimized_video.close()
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error creating optimized video: {e}")
            return video_path  # Return original if optimization fails
    
    def _calculate_optimization_score(self,
                                    video_analysis: Dict[str, Any],
                                    platform_config: PlatformOptimization) -> float:
        """Tính điểm tối ưu hóa"""
        score = 0.0
        max_score = 100.0
        
        # Duration score (30 points)
        duration_diff = abs(video_analysis["duration"] - platform_config.optimal_duration)
        duration_score = max(0, 30 - (duration_diff / 10) * 5)
        score += duration_score
        
        # Resolution score (30 points)
        if video_analysis["resolution"] == platform_config.optimal_resolution:
            score += 30
        else:
            score += 15  # Partial credit for different resolution
        
        # Aspect ratio score (20 points)
        optimal_ratio = platform_config.optimal_resolution[0] / platform_config.optimal_resolution[1]
        current_ratio = video_analysis["aspect_ratio"]
        ratio_diff = abs(current_ratio - optimal_ratio)
        ratio_score = max(0, 20 - ratio_diff * 10)
        score += ratio_score
        
        # File size score (20 points)
        file_size_mb = video_analysis["file_size"] / (1024 * 1024)
        if file_size_mb < 100:  # Less than 100MB
            score += 20
        elif file_size_mb < 500:  # Less than 500MB
            score += 15
        else:
            score += 10
        
        return min(score, max_score)
    
    def generate_marketing_strategy(self,
                                  video_analysis: Dict[str, Any],
                                  target_product: str,
                                  budget: float = 1000) -> Dict[str, Any]:
        """
        Tạo chiến lược marketing toàn diện
        
        Args:
            video_analysis: Phân tích video
            target_product: Sản phẩm mục tiêu
            budget: Ngân sách marketing
            
        Returns:
            Dict[str, Any]: Chiến lược marketing
        """
        strategy = {
            "product": target_product,
            "budget": budget,
            "platforms": {},
            "timeline": {},
            "metrics": {},
            "optimization_plan": {}
        }
        
        # Platform strategy
        for platform, config in self.platform_optimizations.items():
            platform_strategy = {
                "budget_allocation": self._calculate_budget_allocation(platform, budget),
                "posting_schedule": self._create_posting_schedule(platform),
                "content_adaptations": self._get_content_adaptations(platform, target_product),
                "engagement_tactics": config.engagement_tactics,
                "success_metrics": self._define_success_metrics(platform)
            }
            strategy["platforms"][platform] = platform_strategy
        
        # Timeline
        strategy["timeline"] = self._create_marketing_timeline()
        
        # Metrics
        strategy["metrics"] = self._define_overall_metrics()
        
        # Optimization plan
        strategy["optimization_plan"] = self._create_optimization_plan()
        
        return strategy
    
    def _calculate_budget_allocation(self, platform: str, total_budget: float) -> Dict[str, float]:
        """Tính toán phân bổ ngân sách"""
        allocations = {
            "youtube": {"ads": 0.4, "production": 0.3, "promotion": 0.3},
            "tiktok": {"ads": 0.5, "production": 0.2, "promotion": 0.3},
            "instagram": {"ads": 0.4, "production": 0.3, "promotion": 0.3},
            "facebook": {"ads": 0.6, "production": 0.2, "promotion": 0.2}
        }
        
        platform_allocation = allocations.get(platform, {"ads": 0.4, "production": 0.3, "promotion": 0.3})
        
        return {
            "ads": total_budget * platform_allocation["ads"],
            "production": total_budget * platform_allocation["production"],
            "promotion": total_budget * platform_allocation["promotion"]
        }
    
    def _create_posting_schedule(self, platform: str) -> Dict[str, Any]:
        """Tạo lịch đăng bài"""
        schedules = {
            "youtube": {
                "frequency": "2-3 times per week",
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["14:00", "20:00", "22:00"]
            },
            "tiktok": {
                "frequency": "1-2 times per day",
                "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "best_times": ["18:00", "19:00", "20:00", "21:00"]
            },
            "instagram": {
                "frequency": "1 time per day",
                "best_days": ["Monday", "Wednesday", "Friday", "Sunday"],
                "best_times": ["11:00", "14:00", "17:00", "19:00"]
            },
            "facebook": {
                "frequency": "3-4 times per week",
                "best_days": ["Tuesday", "Wednesday", "Thursday", "Friday"],
                "best_times": ["13:00", "15:00", "18:00", "21:00"]
            }
        }
        
        return schedules.get(platform, schedules["youtube"])
    
    def _get_content_adaptations(self, platform: str, product: str) -> List[str]:
        """Lấy các thích ứng nội dung cho platform"""
        adaptations = {
            "youtube": [
                "Create detailed product demonstrations",
                "Add timestamps in description",
                "Include product links in description",
                "Create playlists for related content"
            ],
            "tiktok": [
                "Create quick product showcases",
                "Use trending sounds and effects",
                "Focus on visual appeal",
                "Keep text minimal and impactful"
            ],
            "instagram": [
                "Create visually appealing carousels",
                "Use Stories for behind-the-scenes",
                "Create Reels with product highlights",
                "Use high-quality product photos"
            ],
            "facebook": [
                "Create longer-form content",
                "Use Facebook Live for demonstrations",
                "Create Facebook Groups for community",
                "Share customer testimonials"
            ]
        }
        
        return adaptations.get(platform, adaptations["youtube"])
    
    def _define_success_metrics(self, platform: str) -> Dict[str, Any]:
        """Định nghĩa metrics thành công cho platform"""
        metrics = {
            "youtube": {
                "views": {"target": 10000, "good": 5000, "excellent": 50000},
                "engagement_rate": {"target": 0.05, "good": 0.03, "excellent": 0.08},
                "subscribers": {"target": 100, "good": 50, "excellent": 500},
                "watch_time": {"target": 60, "good": 30, "excellent": 120}
            },
            "tiktok": {
                "views": {"target": 100000, "good": 50000, "excellent": 1000000},
                "likes": {"target": 5000, "good": 2500, "excellent": 50000},
                "shares": {"target": 500, "good": 250, "excellent": 5000},
                "comments": {"target": 200, "good": 100, "excellent": 2000}
            },
            "instagram": {
                "likes": {"target": 1000, "good": 500, "excellent": 10000},
                "comments": {"target": 50, "good": 25, "excellent": 500},
                "shares": {"target": 100, "good": 50, "excellent": 1000},
                "saves": {"target": 200, "good": 100, "excellent": 2000}
            },
            "facebook": {
                "likes": {"target": 500, "good": 250, "excellent": 5000},
                "comments": {"target": 25, "good": 12, "excellent": 250},
                "shares": {"target": 50, "good": 25, "excellent": 500},
                "clicks": {"target": 100, "good": 50, "excellent": 1000}
            }
        }
        
        return metrics.get(platform, metrics["youtube"])
    
    def _create_marketing_timeline(self) -> Dict[str, Any]:
        """Tạo timeline marketing"""
        return {
            "week_1": {
                "focus": "Content creation and platform setup",
                "tasks": [
                    "Create optimized videos for each platform",
                    "Set up social media accounts",
                    "Create content calendar",
                    "Prepare initial posts"
                ]
            },
            "week_2": {
                "focus": "Launch and initial promotion",
                "tasks": [
                    "Launch videos on all platforms",
                    "Start paid advertising campaigns",
                    "Begin community engagement",
                    "Monitor initial performance"
                ]
            },
            "week_3": {
                "focus": "Optimization and scaling",
                "tasks": [
                    "Analyze performance data",
                    "Optimize underperforming content",
                    "Scale successful campaigns",
                    "A/B test different approaches"
                ]
            },
            "week_4": {
                "focus": "Analysis and planning",
                "tasks": [
                    "Complete performance analysis",
                    "Plan next month's strategy",
                    "Adjust budget allocation",
                    "Create success reports"
                ]
            }
        }
    
    def _define_overall_metrics(self) -> Dict[str, Any]:
        """Định nghĩa metrics tổng thể"""
        return {
            "primary_metrics": {
                "total_reach": {"target": 100000, "good": 50000, "excellent": 500000},
                "engagement_rate": {"target": 0.05, "good": 0.03, "excellent": 0.08},
                "conversion_rate": {"target": 0.02, "good": 0.01, "excellent": 0.05},
                "cost_per_acquisition": {"target": 50, "good": 30, "excellent": 20}
            },
            "secondary_metrics": {
                "brand_awareness": "Survey-based measurement",
                "customer_satisfaction": "Review and rating analysis",
                "return_on_investment": "Revenue vs. marketing spend",
                "customer_lifetime_value": "Long-term customer analysis"
            }
        }
    
    def _create_optimization_plan(self) -> Dict[str, Any]:
        """Tạo kế hoạch tối ưu hóa"""
        return {
            "content_optimization": {
                "frequency": "Weekly",
                "focus_areas": [
                    "A/B test different video lengths",
                    "Test various thumbnail designs",
                    "Experiment with different posting times",
                    "Try different hashtag combinations"
                ]
            },
            "audience_optimization": {
                "frequency": "Bi-weekly",
                "focus_areas": [
                    "Analyze audience demographics",
                    "Adjust targeting parameters",
                    "Create audience-specific content",
                    "Optimize for high-value segments"
                ]
            },
            "budget_optimization": {
                "frequency": "Monthly",
                "focus_areas": [
                    "Reallocate budget to best-performing platforms",
                    "Adjust bid strategies",
                    "Optimize ad placements",
                    "Test new advertising formats"
                ]
            }
        }
    
    def save_marketing_strategy(self, strategy: Dict[str, Any], output_dir: Path) -> Path:
        """Lưu chiến lược marketing"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        strategy_file = output_dir / f"marketing_strategy_{timestamp}.json"
        
        with open(strategy_file, 'w', encoding='utf-8') as f:
            json.dump(strategy, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Marketing strategy saved to: {strategy_file}")
        return strategy_file

# Example usage
if __name__ == "__main__":
    from configs.config import MARKETING_CONFIG
    
    optimizer = MarketingOptimizer(MARKETING_CONFIG)
    
    # Analyze a video
    video_analysis = {
        "duration": 120,
        "resolution": (1920, 1080),
        "fps": 30,
        "aspect_ratio": 16/9,
        "file_size": 50 * 1024 * 1024  # 50MB
    }
    
    # Generate marketing strategy
    strategy = optimizer.generate_marketing_strategy(
        video_analysis, "Premium Cooking Course", budget=2000
    )
    
    # Save strategy
    output_dir = Path("outputs/marketing")
    optimizer.save_marketing_strategy(strategy, output_dir)
    
    print("Marketing strategy generated successfully!")
