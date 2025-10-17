"""
Performance Optimizer - Tối ưu hóa hiệu suất và quản lý tài nguyên
"""
import torch
import psutil
import GPUtil
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import gc
import os
from contextlib import contextmanager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Tối ưu hóa hiệu suất hệ thống"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.optimization_settings = self._get_optimization_settings()
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Lấy thông tin hệ thống"""
        info = {
            "cpu": {
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "usage": psutil.cpu_percent(interval=1)
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "usage_percent": psutil.virtual_memory().percent
            },
            "gpu": self._get_gpu_info(),
            "disk": {
                "total": psutil.disk_usage('/').total if os.name != 'nt' else psutil.disk_usage('C:').total,
                "free": psutil.disk_usage('/').free if os.name != 'nt' else psutil.disk_usage('C:').free,
                "usage_percent": psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            }
        }
        
        return info
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Lấy thông tin GPU"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]  # Use first GPU
                return {
                    "name": gpu.name,
                    "memory_total": gpu.memoryTotal,
                    "memory_used": gpu.memoryUsed,
                    "memory_free": gpu.memoryFree,
                    "load": gpu.load,
                    "temperature": gpu.temperature
                }
            else:
                return {"available": False}
        except Exception as e:
            logger.warning(f"Could not get GPU info: {e}")
            return {"available": False}
    
    def _get_optimization_settings(self) -> Dict[str, Any]:
        """Lấy cài đặt tối ưu hóa dựa trên hệ thống"""
        settings = {
            "batch_size": 1,
            "use_half_precision": False,
            "enable_attention_slicing": False,
            "enable_vae_slicing": False,
            "max_workers": 2,
            "memory_cleanup_interval": 5
        }
        
        # Adjust based on system capabilities
        if self.system_info["gpu"].get("available", False):
            gpu_memory = self.system_info["gpu"]["memory_total"]
            
            if gpu_memory >= 8:  # 8GB+ VRAM
                settings.update({
                    "batch_size": 2,
                    "use_half_precision": True,
                    "enable_attention_slicing": False,
                    "enable_vae_slicing": False
                })
            elif gpu_memory >= 4:  # 4-8GB VRAM (GTX 1660 SUPER)
                settings.update({
                    "batch_size": 1,
                    "use_half_precision": True,
                    "enable_attention_slicing": True,
                    "enable_vae_slicing": True
                })
            else:  # <4GB VRAM
                settings.update({
                    "batch_size": 1,
                    "use_half_precision": True,
                    "enable_attention_slicing": True,
                    "enable_vae_slicing": True
                })
        
        # Adjust CPU workers based on CPU count
        cpu_count = self.system_info["cpu"]["count"]
        settings["max_workers"] = min(cpu_count, 4)
        
        return settings
    
    def optimize_torch_settings(self):
        """Tối ưu hóa PyTorch settings"""
        logger.info("🔧 Optimizing PyTorch settings...")
        
        # Set optimal number of threads
        torch.set_num_threads(self.optimization_settings["max_workers"])
        
        # Enable optimizations
        if torch.cuda.is_available():
            # Enable cuDNN benchmark for consistent input sizes
            torch.backends.cudnn.benchmark = True
            
            # Enable memory efficient attention if available
            if hasattr(torch.nn.functional, 'scaled_dot_product_attention'):
                torch.backends.cuda.enable_flash_sdp(True)
            
            logger.info("✅ PyTorch CUDA optimizations enabled")
        else:
            logger.info("⚠️  CUDA not available, using CPU optimizations")
    
    def optimize_model_loading(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Tối ưu hóa cấu hình model loading"""
        optimized_config = model_config.copy()
        
        # Adjust batch size
        optimized_config["batch_size"] = self.optimization_settings["batch_size"]
        
        # Set precision
        if self.optimization_settings["use_half_precision"]:
            optimized_config["torch_dtype"] = torch.float16
        else:
            optimized_config["torch_dtype"] = torch.float32
        
        # Enable memory optimizations
        optimized_config["enable_attention_slicing"] = self.optimization_settings["enable_attention_slicing"]
        optimized_config["enable_vae_slicing"] = self.optimization_settings["enable_vae_slicing"]
        
        logger.info(f"✅ Model config optimized: batch_size={optimized_config['batch_size']}, "
                   f"precision={'half' if self.optimization_settings['use_half_precision'] else 'full'}")
        
        return optimized_config
    
    @contextmanager
    def memory_management(self):
        """Context manager cho quản lý memory"""
        logger.info("🧠 Starting memory management...")
        
        # Clear cache before starting
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        gc.collect()
        
        try:
            yield
        finally:
            # Clean up after completion
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            gc.collect()
            logger.info("✅ Memory cleanup completed")
    
    def monitor_system_resources(self) -> Dict[str, Any]:
        """Monitor tài nguyên hệ thống"""
        current_info = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "gpu_usage": 0,
            "gpu_memory_usage": 0
        }
        
        # Get GPU usage if available
        if self.system_info["gpu"].get("available", False):
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    current_info["gpu_usage"] = gpu.load * 100
                    current_info["gpu_memory_usage"] = (gpu.memoryUsed / gpu.memoryTotal) * 100
            except Exception as e:
                logger.warning(f"Could not get GPU usage: {e}")
        
        return current_info
    
    def check_system_health(self) -> Dict[str, Any]:
        """Kiểm tra sức khỏe hệ thống"""
        health = {
            "status": "healthy",
            "warnings": [],
            "recommendations": []
        }
        
        # Check CPU usage
        cpu_usage = self.system_info["cpu"]["usage"]
        if cpu_usage > 90:
            health["warnings"].append(f"High CPU usage: {cpu_usage}%")
            health["recommendations"].append("Consider reducing parallel tasks")
        
        # Check memory usage
        memory_usage = self.system_info["memory"]["usage_percent"]
        if memory_usage > 85:
            health["warnings"].append(f"High memory usage: {memory_usage}%")
            health["recommendations"].append("Consider reducing batch size or enabling memory optimizations")
        
        # Check GPU usage
        if self.system_info["gpu"].get("available", False):
            gpu_memory_usage = (self.system_info["gpu"]["memory_used"] / self.system_info["gpu"]["memory_total"]) * 100
            if gpu_memory_usage > 90:
                health["warnings"].append(f"High GPU memory usage: {gpu_memory_usage:.1f}%")
                health["recommendations"].append("Consider enabling attention slicing or reducing batch size")
        
        # Check disk space
        disk_usage = self.system_info["disk"]["usage_percent"]
        if disk_usage > 90:
            health["warnings"].append(f"Low disk space: {100-disk_usage:.1f}% free")
            health["recommendations"].append("Consider cleaning up old outputs or using external storage")
        
        # Set status
        if health["warnings"]:
            health["status"] = "warning"
        if len(health["warnings"]) > 3:
            health["status"] = "critical"
        
        return health
    
    def get_optimization_recommendations(self) -> List[str]:
        """Đưa ra khuyến nghị tối ưu hóa"""
        recommendations = []
        
        # GPU recommendations
        if not self.system_info["gpu"].get("available", False):
            recommendations.append("Consider using a GPU for faster processing")
        elif self.system_info["gpu"]["memory_total"] < 4:
            recommendations.append("Consider upgrading to a GPU with more VRAM for better performance")
        
        # Memory recommendations
        if self.system_info["memory"]["total"] < 16 * 1024**3:  # Less than 16GB
            recommendations.append("Consider upgrading to 32GB RAM for better performance")
        
        # CPU recommendations
        if self.system_info["cpu"]["count"] < 8:
            recommendations.append("Consider using a CPU with more cores for parallel processing")
        
        # Storage recommendations
        if self.system_info["disk"]["free"] < 50 * 1024**3:  # Less than 50GB free
            recommendations.append("Consider freeing up disk space or using external storage")
        
        return recommendations
    
    def create_performance_report(self) -> Dict[str, Any]:
        """Tạo báo cáo hiệu suất"""
        report = {
            "system_info": self.system_info,
            "optimization_settings": self.optimization_settings,
            "system_health": self.check_system_health(),
            "recommendations": self.get_optimization_recommendations(),
            "generated_at": "2024-01-01T00:00:00"  # Will be set by caller
        }
        
        return report
    
    def save_performance_report(self, output_dir: Path):
        """Lưu báo cáo hiệu suất"""
        from datetime import datetime
        
        report = self.create_performance_report()
        report["generated_at"] = datetime.now().isoformat()
        
        output_dir.mkdir(parents=True, exist_ok=True)
        report_file = output_dir / "performance_report.json"
        
        import json
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Performance report saved to: {report_file}")
        return report_file

# Example usage
if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    
    # Optimize PyTorch
    optimizer.optimize_torch_settings()
    
    # Check system health
    health = optimizer.check_system_health()
    print(f"System health: {health['status']}")
    
    if health["warnings"]:
        print("Warnings:")
        for warning in health["warnings"]:
            print(f"  - {warning}")
    
    if health["recommendations"]:
        print("Recommendations:")
        for rec in health["recommendations"]:
            print(f"  - {rec}")
    
    # Get optimization recommendations
    recommendations = optimizer.get_optimization_recommendations()
    if recommendations:
        print("\nOptimization recommendations:")
        for rec in recommendations:
            print(f"  - {rec}")
    
    # Save performance report
    optimizer.save_performance_report(Path("outputs"))
