"""
Pipeline Manager - Quản lý và điều phối toàn bộ pipeline
"""
import logging
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import concurrent.futures
from dataclasses import dataclass

from .image_generation import ModelGenerator
from .trend_analysis import TrendAnalyzer
from .content_analysis import ContentAnalyzer
from .script_generation import ScriptGenerator
from .video_production import VideoProducer
from .video_editing import VideoEditor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PipelineConfig:
    """Cấu hình pipeline"""
    keywords: List[str]
    target_product: str
    video_duration: int
    output_dir: Path
    max_parallel_tasks: int = 3
    enable_gpu: bool = True
    quality_preset: str = "high"  # low, medium, high, ultra

class PipelineManager:
    """Quản lý và điều phối pipeline AI Video Marketing"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.components = {}
        self._initialize_components()
        
    def _initialize_components(self):
        """Khởi tạo các component"""
        try:
            logger.info("Initializing pipeline components...")
            
            self.components = {
                'model_generator': ModelGenerator(self.config['ai']['stable_diffusion']),
                'trend_analyzer': TrendAnalyzer(self.config['trend']),
                'content_analyzer': ContentAnalyzer(self.config['ai']['openai']),
                'script_generator': ScriptGenerator(self.config['ai']['openai']),
                'video_producer': VideoProducer(self.config['video']),
                'video_editor': VideoEditor(self.config['video'])
            }
            
            logger.info("✓ All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    async def run_async_pipeline(self, pipeline_config: PipelineConfig) -> Dict[str, Any]:
        """
        Chạy pipeline bất đồng bộ để tối ưu hiệu suất
        
        Args:
            pipeline_config: Cấu hình pipeline
            
        Returns:
            Dict[str, Any]: Kết quả pipeline
        """
        logger.info("🚀 Starting async pipeline...")
        
        pipeline_results = {
            "pipeline_info": {
                "started_at": datetime.now().isoformat(),
                "config": pipeline_config.__dict__,
                "mode": "async"
            },
            "steps": {}
        }
        
        try:
            # Step 1: Trend Analysis (có thể chạy song song với model generation)
            logger.info("📊 Step 1: Starting trend analysis...")
            trend_task = asyncio.create_task(
                self._run_trend_analysis_async(pipeline_config)
            )
            
            # Step 2: Model Generation (chạy song song)
            logger.info("👤 Step 2: Starting model generation...")
            model_task = asyncio.create_task(
                self._run_model_generation_async(pipeline_config)
            )
            
            # Chờ cả hai task hoàn thành
            trend_result, model_result = await asyncio.gather(trend_task, model_task)
            
            pipeline_results["steps"]["trend_analysis"] = trend_result
            pipeline_results["steps"]["model_generation"] = model_result
            
            # Step 3: Content Analysis (phụ thuộc vào trend analysis)
            logger.info("🔍 Step 3: Starting content analysis...")
            content_result = await self._run_content_analysis_async(
                pipeline_config, trend_result
            )
            pipeline_results["steps"]["content_analysis"] = content_result
            
            # Step 4: Script Generation (phụ thuộc vào trend và content analysis)
            logger.info("📝 Step 4: Starting script generation...")
            script_result = await self._run_script_generation_async(
                pipeline_config, trend_result, content_result
            )
            pipeline_results["steps"]["script_generation"] = script_result
            
            # Step 5: Video Production (phụ thuộc vào script và model images)
            logger.info("🎬 Step 5: Starting video production...")
            video_result = await self._run_video_production_async(
                pipeline_config, script_result, model_result
            )
            pipeline_results["steps"]["video_production"] = video_result
            
            # Step 6: Video Editing (phụ thuộc vào video production)
            logger.info("✂️ Step 6: Starting video editing...")
            editing_result = await self._run_video_editing_async(
                pipeline_config, script_result, video_result
            )
            pipeline_results["steps"]["video_editing"] = editing_result
            
            # Pipeline completed
            pipeline_results["pipeline_info"]["completed_at"] = datetime.now().isoformat()
            pipeline_results["pipeline_info"]["status"] = "completed"
            pipeline_results["pipeline_info"]["success"] = True
            
            logger.info("🎉 Async pipeline completed successfully!")
            return pipeline_results
            
        except Exception as e:
            logger.error(f"❌ Async pipeline failed: {e}")
            pipeline_results["pipeline_info"]["status"] = "failed"
            pipeline_results["pipeline_info"]["error"] = str(e)
            pipeline_results["pipeline_info"]["completed_at"] = datetime.now().isoformat()
            raise
    
    async def _run_trend_analysis_async(self, config: PipelineConfig) -> Dict[str, Any]:
        """Chạy trend analysis bất đồng bộ"""
        def run_trend_analysis():
            analyzer = self.components['trend_analyzer']
            videos = analyzer.search_trending_keywords(config.keywords, max_results=50)
            analysis = analyzer.analyze_trending_patterns(videos)
            
            # Save results
            output_dir = config.output_dir / "trend_analysis"
            output_dir.mkdir(parents=True, exist_ok=True)
            analyzer.save_analysis(videos, analysis, output_dir)
            
            return {
                "status": "completed",
                "videos_found": len(videos),
                "output_dir": str(output_dir)
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_trend_analysis)
        
        return result
    
    async def _run_model_generation_async(self, config: PipelineConfig) -> Dict[str, Any]:
        """Chạy model generation bất đồng bộ"""
        def run_model_generation():
            generator = self.components['model_generator']
            
            model_config = {
                "gender": "female",
                "age": "young adult",
                "ethnicity": "asian",
                "style": "professional",
                "setting": "studio",
                "clothing": "business casual"
            }
            
            output_dir = config.output_dir / "model_images"
            portfolio = generator.create_model_portfolio(model_config, output_dir)
            
            # Count generated images
            total_images = sum(len(paths) for paths in portfolio["images"].values())
            
            return {
                "status": "completed",
                "images_generated": total_images,
                "output_dir": str(output_dir)
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_model_generation)
        
        return result
    
    async def _run_content_analysis_async(self, 
                                        config: PipelineConfig,
                                        trend_result: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy content analysis bất đồng bộ"""
        def run_content_analysis():
            analyzer = self.components['content_analyzer']
            
            # Load trend analysis results
            trend_file = Path(trend_result["output_dir"]) / "trend_analysis_*.json"
            # Implementation would load the actual trend data here
            
            # For now, use mock data
            mock_videos = [{"title": f"Video {i}", "description": f"Description {i}"} 
                          for i in range(10)]
            
            output_dir = config.output_dir / "content_analysis"
            results = analyzer.batch_analyze_videos(mock_videos, output_dir)
            
            return {
                "status": "completed",
                "videos_analyzed": len(results),
                "output_dir": str(output_dir)
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_content_analysis)
        
        return result
    
    async def _run_script_generation_async(self,
                                         config: PipelineConfig,
                                         trend_result: Dict[str, Any],
                                         content_result: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy script generation bất đồng bộ"""
        def run_script_generation():
            generator = self.components['script_generator']
            
            # Mock trend analysis data
            trend_analysis = {"videos": [], "analysis": {}}
            content_analysis = []
            
            script = generator.generate_video_script(
                trend_analysis=trend_analysis,
                content_analysis=content_analysis,
                target_product=config.target_product,
                video_duration=config.video_duration
            )
            
            # Save script
            output_dir = config.output_dir / "scripts"
            output_dir.mkdir(parents=True, exist_ok=True)
            script_file = generator.save_script(script, output_dir)
            
            return {
                "status": "completed",
                "output_file": str(script_file),
                "success_probability": script.get("insights", {}).get("success_probability", 0)
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_script_generation)
        
        return result
    
    async def _run_video_production_async(self,
                                        config: PipelineConfig,
                                        script_result: Dict[str, Any],
                                        model_result: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy video production bất đồng bộ"""
        def run_video_production():
            producer = self.components['video_producer']
            
            # Load script
            script_file = Path(script_result["output_file"])
            with open(script_file, 'r', encoding='utf-8') as f:
                script = json.load(f)
            
            # Load model images
            model_images = []
            model_dir = Path(model_result["output_dir"])
            for img_file in model_dir.rglob("*.png"):
                from PIL import Image
                model_images.append(Image.open(img_file))
            
            # Create video
            output_path = config.output_dir / "main_video.mp4"
            video_info = producer.create_video_from_script(script, model_images, output_path)
            
            return {
                "status": "completed",
                "output_file": str(output_path),
                "duration": video_info["duration"]
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_video_production)
        
        return result
    
    async def _run_video_editing_async(self,
                                     config: PipelineConfig,
                                     script_result: Dict[str, Any],
                                     video_result: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy video editing bất đồng bộ"""
        def run_video_editing():
            editor = self.components['video_editor']
            
            # Load script
            script_file = Path(script_result["output_file"])
            with open(script_file, 'r', encoding='utf-8') as f:
                script = json.load(f)
            
            # Edit video
            video_path = video_result["output_file"]
            final_video_info = editor.create_final_video(
                [video_path], script, config.output_dir / "final_video.mp4"
            )
            
            # Create short clips
            short_clips = editor.create_short_clips(
                video_path, script, config.output_dir / "short_clips"
            )
            
            return {
                "status": "completed",
                "output_files": final_video_info["output_paths"],
                "short_clips_created": len(short_clips)
            }
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, run_video_editing)
        
        return result
    
    def run_batch_pipeline(self, 
                          pipeline_configs: List[PipelineConfig]) -> List[Dict[str, Any]]:
        """
        Chạy nhiều pipeline song song
        
        Args:
            pipeline_configs: Danh sách cấu hình pipeline
            
        Returns:
            List[Dict[str, Any]]: Kết quả của tất cả pipeline
        """
        logger.info(f"🚀 Starting batch pipeline with {len(pipeline_configs)} configurations...")
        
        async def run_all_pipelines():
            tasks = []
            for config in pipeline_configs:
                task = asyncio.create_task(self.run_async_pipeline(config))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        # Run all pipelines
        results = asyncio.run(run_all_pipelines())
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Pipeline {i+1} failed: {result}")
                processed_results.append({
                    "pipeline_index": i,
                    "status": "failed",
                    "error": str(result)
                })
            else:
                result["pipeline_index"] = i
                processed_results.append(result)
        
        logger.info(f"🎉 Batch pipeline completed: {len(processed_results)} results")
        return processed_results
    
    def get_pipeline_status(self, output_dir: Path) -> Dict[str, Any]:
        """
        Lấy trạng thái pipeline từ thư mục output
        
        Args:
            output_dir: Thư mục output
            
        Returns:
            Dict[str, Any]: Trạng thái pipeline
        """
        status = {
            "output_dir": str(output_dir),
            "exists": output_dir.exists(),
            "steps_completed": [],
            "files_generated": []
        }
        
        if not output_dir.exists():
            return status
        
        # Check for completed steps
        step_dirs = [
            "trend_analysis",
            "content_analysis", 
            "model_images",
            "scripts",
            "short_clips"
        ]
        
        for step_dir in step_dirs:
            if (output_dir / step_dir).exists():
                status["steps_completed"].append(step_dir)
        
        # Check for generated files
        for file_path in output_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.mp4', '.json', '.png', '.jpg']:
                status["files_generated"].append(str(file_path.relative_to(output_dir)))
        
        return status

# Example usage
if __name__ == "__main__":
    from configs.config import AI_CONFIG, TREND_CONFIG, VIDEO_CONFIG
    
    # Initialize pipeline manager
    config = {
        'ai': AI_CONFIG,
        'trend': TREND_CONFIG,
        'video': VIDEO_CONFIG
    }
    
    manager = PipelineManager(config)
    
    # Create pipeline config
    pipeline_config = PipelineConfig(
        keywords=["cooking", "tips", "viral"],
        target_product="Cooking Course",
        video_duration=60,
        output_dir=Path("outputs/test_pipeline")
    )
    
    # Run async pipeline
    async def main():
        result = await manager.run_async_pipeline(pipeline_config)
        print("Pipeline completed:", result)
    
    asyncio.run(main())
