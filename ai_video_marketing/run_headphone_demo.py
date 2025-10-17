"""
Run Headphone Demo with Asian Male Model
"""
import sys
from pathlib import Path
import json
import subprocess
import os

def install_dependencies():
    """Cai dat dependencies can thiet"""
    print("Installing dependencies...")
    
    dependencies = [
        "torch",
        "torchvision", 
        "transformers",
        "diffusers",
        "opencv-python",
        "moviepy",
        "pillow",
        "numpy",
        "requests"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"✓ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {dep}: {e}")
            return False
    
    return True

def run_headphone_demo():
    """Chay demo tai nghe voi nguoi mau nam chau A"""
    
    print("DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A")
    print("=" * 50)
    
    # Doc cau hinh tu file
    config_file = Path("outputs/headphone_demo_20251017_214847/demo_config.json")
    
    if not config_file.exists():
        print("Config file not found. Please run headphone_demo.py first.")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("Cau hinh nguoi mau:")
    model_config = config["model_config"]
    for key, value in model_config.items():
        print(f"   {key}: {value}")
    
    print(f"\nSan pham: {config['script']['product']}")
    print(f"Thoi luong: {config['script']['duration']} giay")
    print(f"Keywords: {', '.join(config['keywords'])}")
    
    # Tao lenh chay
    keywords_str = " ".join([f"'{kw}'" for kw in config['keywords'][:3]])  # Chi lay 3 keywords dau
    product = config['script']['product']
    duration = config['script']['duration']
    
    command = [
        sys.executable, "main.py",
        "--mode", "demo",
        "--keywords", *config['keywords'][:3],
        "--product", product,
        "--duration", str(duration)
    ]
    
    print(f"\nChay lenh: {' '.join(command)}")
    
    try:
        # Chay pipeline
        result = subprocess.run(command, cwd=Path.cwd(), 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✓ Pipeline chay thanh cong!")
            print("Output:")
            print(result.stdout)
        else:
            print("✗ Pipeline that bai!")
            print("Error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Loi khi chay pipeline: {e}")
        return False
    
    return True

def check_system_requirements():
    """Kiem tra yeu cau he thong"""
    print("Kiem tra yeu cau he thong...")
    
    # Kiem tra Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"✗ Python 3.8+ required, current: {python_version.major}.{python_version.minor}")
        return False
    print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Kiem tra GPU
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✓ GPU available: {gpu_name} ({gpu_memory:.1f}GB VRAM)")
        else:
            print("⚠ GPU not available, will use CPU (slower)")
    except ImportError:
        print("⚠ PyTorch not installed yet")
    
    # Kiem tra FFmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ FFmpeg available")
        else:
            print("⚠ FFmpeg not found - required for video processing")
    except FileNotFoundError:
        print("⚠ FFmpeg not found - required for video processing")
    
    return True

def main():
    """Main function"""
    
    print("HEADPHONE DEMO RUNNER")
    print("=" * 30)
    
    # Kiem tra yeu cau he thong
    if not check_system_requirements():
        print("System requirements not met. Please check and try again.")
        return
    
    # Hoi nguoi dung co muon cai dat dependencies khong
    choice = input("\nBan co muon cai dat dependencies? (y/n): ")
    if choice.lower() == 'y':
        if not install_dependencies():
            print("Failed to install dependencies. Please install manually.")
            return
    
    # Chay demo
    print("\nBat dau chay demo...")
    if run_headphone_demo():
        print("\n✓ Demo hoan thanh thanh cong!")
        print("Kiem tra thu muc outputs/ de xem ket qua")
    else:
        print("\n✗ Demo that bai!")
        print("Vui long kiem tra loi va thu lai")

if __name__ == "__main__":
    main()
