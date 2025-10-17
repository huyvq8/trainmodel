"""
AI Video Marketing System - Main Pipeline
Hệ thống tạo video marketing tự động với AI
"""
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import argparse

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import modules
from image_generation.model_generator import ModelGenerator
from trend_analysis.trend_analyzer import TrendAnalyzer
from content_analysis.content_analyzer import ContentAnalyzer
from script_generation.script_generator import ScriptGenerator
from video_production.video_producer import VideoProducer
from video_editing.video_editor import VideoEditor
from pipeline_manager import PipelineManager, PipelineConfig
from performance_optimizer import PerformanceOptimizer
from marketing_optimizer import MarketingOptimizer

# Import config
from configs.config import (
    AI_CONFIG, TREND_CONFIG, CONTENT_CONFIG, 
    VIDEO_CONFIG, MARKETING_CONFIG, OUTPUTS_DIR
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIVideoMarketingSystem:
    """Hệ thống AI Video Marketing hoàn chỉnh"""
    
    def __init__(self):
        self.model_generator = None
        self.trend_analyzer = None
        self.content_analyzer = None
        self.script_generator = None
        self.video_producer = None
        self.video_editor = None
        self.pipeline_manager = None
        self.performance_optimizer = None
        self.marketing_optimizer = None
        
        # Initialize components
        self._initialize_components()
        
    def _initialize_components(self):
        """Khởi tạo các component"""
        try:
            logger.info("Initializing AI Video Marketing System...")
            
            # Initialize model generator
            self.model_generator = ModelGenerator(AI_CONFIG["stable_diffusion"])
            logger.info("✓ Model Generator initialized")
            
            # Initialize trend analyzer
            self.trend_analyzer = TrendAnalyzer(TREND_CONFIG)
            logger.info("✓ Trend Analyzer initialized")
            
            # Initialize content analyzer
            self.content_analyzer = ContentAnalyzer(AI_CONFIG["openai"])
            logger.info("✓ Content Analyzer initialized")
            
            # Initialize script generator
            self.script_generator = ScriptGenerator(AI_CONFIG["openai"])
            logger.info("✓ Script Generator initialized")
            
            # Initialize video producer
            self.video_producer = VideoProducer(VIDEO_CONFIG)
            logger.info("✓ Video Producer initialized")
            
            # Initialize video editor
            self.video_editor = VideoEditor(VIDEO_CONFIG)
            logger.info("✓ Video Editor initialized")
            
            # Initialize pipeline manager
            pipeline_config = {
                'ai': AI_CONFIG,
                'trend': TREND_CONFIG,
                'video': VIDEO_CONFIG
            }
            self.pipeline_manager = PipelineManager(pipeline_config)
            logger.info("✓ Pipeline Manager initialized")
            
            # Initialize performance optimizer
            self.performance_optimizer = PerformanceOptimizer()
            logger.info("✓ Performance Optimizer initialized")
            
            # Initialize marketing optimizer
            self.marketing_optimizer = MarketingOptimizer(MARKETING_CONFIG)
            logger.info("✓ Marketing Optimizer initialized")
            
            logger.info("🎉 All components initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    def run_full_pipeline(self, 
                         keywords: List[str],
                         target_product: str = "",
                         video_duration: int = 60,
                         output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Chạy toàn bộ pipeline tạo video marketing
        
        Args:
            keywords: Danh sách từ khóa trending
            target_product: Sản phẩm mục tiêu
            video_duration: Thời lượng video (giây)
            output_dir: Thư mục lưu kết quả
            
        Returns:
            Dict[str, Any]: Kết quả toàn bộ pipeline
        """
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = OUTPUTS_DIR / f"pipeline_run_{timestamp}"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🚀 Starting AI Video Marketing Pipeline...")
        logger.info(f"Keywords: {keywords}")
        logger.info(f"Target Product: {target_product}")
        logger.info(f"Video Duration: {video_duration}s")
        logger.info(f"Output Directory: {output_dir}")
        
        pipeline_results = {
            "pipeline_info": {
                "started_at": datetime.now().isoformat(),
                "keywords": keywords,
                "target_product": target_product,
                "video_duration": video_duration,
                "output_dir": str(output_dir)
            },
            "steps": {}
        }
        
        try:
            # Step 1: Tìm kiếm xu hướng
            logger.info("📊 Step 1: Analyzing trends...")
            trending_videos = self.trend_analyzer.search_trending_keywords(
                keywords, max_results=50
            )
            trend_analysis = self.trend_analyzer.analyze_trending_patterns(trending_videos)
            
            # Save trend analysis
            trend_file = output_dir / "trend_analysis.json"
            with open(trend_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "videos": [vars(video) for video in trending_videos],
                    "analysis": trend_analysis
                }, f, indent=2, ensure_ascii=False)
            
            pipeline_results["steps"]["trend_analysis"] = {
                "status": "completed",
                "videos_found": len(trending_videos),
                "output_file": str(trend_file)
            }
            logger.info(f"✓ Found {len(trending_videos)} trending videos")
            
            # Step 2: Phân tích nội dung
            logger.info("🔍 Step 2: Analyzing content...")
            content_analysis = self.content_analyzer.batch_analyze_videos(
                [vars(video) for video in trending_videos[:10]],  # Analyze top 10
                output_dir / "content_analysis"
            )
            
            pipeline_results["steps"]["content_analysis"] = {
                "status": "completed",
                "videos_analyzed": len(content_analysis),
                "output_dir": str(output_dir / "content_analysis")
            }
            logger.info(f"✓ Analyzed {len(content_analysis)} videos")
            
            # Step 3: Tạo ảnh người mẫu
            logger.info("👤 Step 3: Generating model images...")
            model_config = {
                "gender": "female",
                "age": "young adult",
                "ethnicity": "asian",
                "style": "professional",
                "setting": "studio",
                "clothing": "business casual"
            }
            
            model_portfolio = self.model_generator.create_model_portfolio(
                model_config, output_dir / "model_images"
            )
            
            # Get model images
            model_images = []
            for variation_name, image_paths in model_portfolio["images"].items():
                for image_path in image_paths:
                    from PIL import Image
                    model_images.append(Image.open(image_path))
            
            pipeline_results["steps"]["model_generation"] = {
                "status": "completed",
                "images_generated": len(model_images),
                "output_dir": str(output_dir / "model_images")
            }
            logger.info(f"✓ Generated {len(model_images)} model images")
            
            # Step 4: Tạo kịch bản
            logger.info("📝 Step 4: Generating script...")
            script = self.script_generator.generate_video_script(
                trend_analysis={"videos": [vars(v) for v in trending_videos], "analysis": trend_analysis},
                content_analysis=content_analysis,
                target_product=target_product,
                video_duration=video_duration
            )
            
            # Save script
            script_file = output_dir / "video_script.json"
            with open(script_file, 'w', encoding='utf-8') as f:
                json.dump(script, f, indent=2, ensure_ascii=False)
            
            pipeline_results["steps"]["script_generation"] = {
                "status": "completed",
                "output_file": str(script_file),
                "success_probability": script.get("insights", {}).get("success_probability", 0)
            }
            logger.info("✓ Script generated successfully")
            
            # Step 5: Sản xuất video
            logger.info("🎬 Step 5: Producing video...")
            video_output_path = output_dir / "main_video.mp4"
            video_info = self.video_producer.create_video_from_script(
                script, model_images, video_output_path
            )
            
            pipeline_results["steps"]["video_production"] = {
                "status": "completed",
                "output_file": str(video_output_path),
                "duration": video_info["duration"]
            }
            logger.info("✓ Video produced successfully")
            
            # Step 6: Chỉnh sửa video
            logger.info("✂️ Step 6: Editing final video...")
            final_video_info = self.video_editor.create_final_video(
                [str(video_output_path)], script, output_dir / "final_video.mp4"
            )
            
            pipeline_results["steps"]["video_editing"] = {
                "status": "completed",
                "output_files": final_video_info["output_paths"]
            }
            logger.info("✓ Final video edited successfully")
            
            # Step 7: Tạo clips ngắn
            logger.info("📱 Step 7: Creating short clips...")
            short_clips = self.video_editor.create_short_clips(
                str(video_output_path), script, output_dir / "short_clips"
            )
            
            pipeline_results["steps"]["short_clips"] = {
                "status": "completed",
                "clips_created": len(short_clips),
                "output_dir": str(output_dir / "short_clips")
            }
            logger.info(f"✓ Created {len(short_clips)} short clips")
            
            # Pipeline completed
            pipeline_results["pipeline_info"]["completed_at"] = datetime.now().isoformat()
            pipeline_results["pipeline_info"]["status"] = "completed"
            pipeline_results["pipeline_info"]["success"] = True
            
            # Save pipeline results
            results_file = output_dir / "pipeline_results.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_results, f, indent=2, ensure_ascii=False)
            
            logger.info("🎉 Pipeline completed successfully!")
            logger.info(f"📁 All results saved to: {output_dir}")
            
            return pipeline_results
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            pipeline_results["pipeline_info"]["status"] = "failed"
            pipeline_results["pipeline_info"]["error"] = str(e)
            pipeline_results["pipeline_info"]["completed_at"] = datetime.now().isoformat()
            
            # Save error results
            results_file = output_dir / "pipeline_results.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_results, f, indent=2, ensure_ascii=False)
            
            raise
    
    def run_quick_demo(self, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Chạy demo nhanh với dữ liệu mẫu
        
        Args:
            output_dir: Thư mục lưu kết quả
            
        Returns:
            Dict[str, Any]: Kết quả demo
        """
        logger.info("🚀 Running Quick Demo...")
        
        # Demo keywords
        demo_keywords = ["cooking tips", "healthy recipes", "quick meals"]
        demo_product = "Premium Cooking Course"
        
        return self.run_full_pipeline(
            keywords=demo_keywords,
            target_product=demo_product,
            video_duration=45,
            output_dir=output_dir
        )
    
    def run_custom_pipeline(self, 
                          config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chạy pipeline với cấu hình tùy chỉnh
        
        Args:
            config: Cấu hình pipeline
            
        Returns:
            Dict[str, Any]: Kết quả pipeline
        """
        logger.info("🚀 Running Custom Pipeline...")
        
        return self.run_full_pipeline(
            keywords=config.get("keywords", ["demo"]),
            target_product=config.get("target_product", ""),
            video_duration=config.get("video_duration", 60),
            output_dir=config.get("output_dir")
        )
    
    async def run_async_pipeline(self, 
                               keywords: List[str],
                               target_product: str = "",
                               video_duration: int = 60,
                               output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Chạy pipeline bất đồng bộ để tối ưu hiệu suất
        
        Args:
            keywords: Danh sách từ khóa trending
            target_product: Sản phẩm mục tiêu
            video_duration: Thời lượng video (giây)
            output_dir: Thư mục lưu kết quả
            
        Returns:
            Dict[str, Any]: Kết quả pipeline
        """
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = OUTPUTS_DIR / f"async_pipeline_{timestamp}"
        
        logger.info("🚀 Starting Async Pipeline...")
        
        # Create pipeline config
        pipeline_config = PipelineConfig(
            keywords=keywords,
            target_product=target_product,
            video_duration=video_duration,
            output_dir=output_dir
        )
        
        # Run async pipeline
        return await self.pipeline_manager.run_async_pipeline(pipeline_config)
    
    def run_batch_pipeline(self, 
                          pipeline_configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chạy nhiều pipeline song song
        
        Args:
            pipeline_configs: Danh sách cấu hình pipeline
            
        Returns:
            List[Dict[str, Any]]: Kết quả của tất cả pipeline
        """
        logger.info(f"🚀 Starting Batch Pipeline with {len(pipeline_configs)} configurations...")
        
        # Convert configs to PipelineConfig objects
        configs = []
        for config in pipeline_configs:
            pipeline_config = PipelineConfig(
                keywords=config.get("keywords", ["demo"]),
                target_product=config.get("target_product", ""),
                video_duration=config.get("video_duration", 60),
                output_dir=config.get("output_dir")
            )
            configs.append(pipeline_config)
        
        # Run batch pipeline
        return self.pipeline_manager.run_batch_pipeline(configs)
    
    def optimize_system_performance(self) -> Dict[str, Any]:
        """
        Tối ưu hóa hiệu suất hệ thống
        
        Returns:
            Dict[str, Any]: Kết quả tối ưu hóa
        """
        logger.info("🔧 Optimizing system performance...")
        
        # Optimize PyTorch settings
        self.performance_optimizer.optimize_torch_settings()
        
        # Check system health
        health = self.performance_optimizer.check_system_health()
        
        # Get recommendations
        recommendations = self.performance_optimizer.get_optimization_recommendations()
        
        # Save performance report
        report_file = self.performance_optimizer.save_performance_report(OUTPUTS_DIR / "performance")
        
        return {
            "system_health": health,
            "recommendations": recommendations,
            "report_file": str(report_file)
        }
    
    def generate_marketing_strategy(self, 
                                  video_path: str,
                                  target_product: str,
                                  budget: float = 1000) -> Dict[str, Any]:
        """
        Tạo chiến lược marketing toàn diện
        
        Args:
            video_path: Đường dẫn video
            target_product: Sản phẩm mục tiêu
            budget: Ngân sách marketing
            
        Returns:
            Dict[str, Any]: Chiến lược marketing
        """
        logger.info("📊 Generating marketing strategy...")
        
        # Analyze video
        video_analysis = self.marketing_optimizer._analyze_video(video_path)
        
        # Generate strategy
        strategy = self.marketing_optimizer.generate_marketing_strategy(
            video_analysis, target_product, budget
        )
        
        # Save strategy
        strategy_file = self.marketing_optimizer.save_marketing_strategy(
            strategy, OUTPUTS_DIR / "marketing"
        )
        
        return {
            "strategy": strategy,
            "strategy_file": str(strategy_file)
        }

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="AI Video Marketing System")
    parser.add_argument("--mode", choices=["demo", "custom", "full", "async", "batch", "optimize", "marketing"], 
                       default="demo", help="Pipeline mode")
    parser.add_argument("--keywords", nargs="+", 
                       default=["cooking", "tips", "viral"], 
                       help="Trending keywords")
    parser.add_argument("--product", type=str, 
                       default="Cooking Course", 
                       help="Target product")
    parser.add_argument("--duration", type=int, 
                       default=60, 
                       help="Video duration in seconds")
    parser.add_argument("--output", type=str, 
                       help="Output directory")
    parser.add_argument("--budget", type=float, 
                       default=1000, 
                       help="Marketing budget")
    parser.add_argument("--video-path", type=str, 
                       help="Path to video for marketing optimization")
    
    args = parser.parse_args()
    
    # Initialize system
    system = AIVideoMarketingSystem()
    
    try:
        if args.mode == "demo":
            # Run quick demo
            output_dir = Path(args.output) if args.output else None
            results = system.run_quick_demo(output_dir)
            
        elif args.mode == "custom":
            # Run with custom config
            config = {
                "keywords": args.keywords,
                "target_product": args.product,
                "video_duration": args.duration,
                "output_dir": Path(args.output) if args.output else None
            }
            results = system.run_custom_pipeline(config)
            
        elif args.mode == "full":
            # Run full pipeline
            output_dir = Path(args.output) if args.output else None
            results = system.run_full_pipeline(
                keywords=args.keywords,
                target_product=args.product,
                video_duration=args.duration,
                output_dir=output_dir
            )
            
        elif args.mode == "async":
            # Run async pipeline
            import asyncio
            output_dir = Path(args.output) if args.output else None
            results = asyncio.run(system.run_async_pipeline(
                keywords=args.keywords,
                target_product=args.product,
                video_duration=args.duration,
                output_dir=output_dir
            ))
            
        elif args.mode == "batch":
            # Run batch pipeline
            configs = [
                {
                    "keywords": args.keywords,
                    "target_product": args.product,
                    "video_duration": args.duration,
                    "output_dir": Path(args.output) / "batch_1" if args.output else None
                },
                {
                    "keywords": [kw + " tips" for kw in args.keywords],
                    "target_product": args.product + " Advanced",
                    "video_duration": args.duration + 30,
                    "output_dir": Path(args.output) / "batch_2" if args.output else None
                }
            ]
            results = system.run_batch_pipeline(configs)
            
        elif args.mode == "optimize":
            # Optimize system performance
            results = system.optimize_system_performance()
            
        elif args.mode == "marketing":
            # Generate marketing strategy
            if not args.video_path:
                print("❌ --video-path is required for marketing mode")
                sys.exit(1)
            results = system.generate_marketing_strategy(
                video_path=args.video_path,
                target_product=args.product,
                budget=args.budget
            )
        
        # Print summary
        print("\n" + "="*50)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"📁 Output Directory: {results['pipeline_info']['output_dir']}")
        print(f"⏱️  Duration: {results['pipeline_info'].get('completed_at', 'N/A')}")
        print(f"📊 Videos Found: {results['steps']['trend_analysis']['videos_found']}")
        print(f"🔍 Videos Analyzed: {results['steps']['content_analysis']['videos_analyzed']}")
        print(f"👤 Model Images: {results['steps']['model_generation']['images_generated']}")
        print(f"📝 Script Success Rate: {results['steps']['script_generation']['success_probability']:.1f}/10")
        print(f"🎬 Video Duration: {results['steps']['video_production']['duration']:.1f}s")
        print(f"📱 Short Clips: {results['steps']['short_clips']['clips_created']}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

