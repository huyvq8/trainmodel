"""
Install Dependencies and Run Headphone Demo
"""
import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Cai dat dependencies"""
    print("CAI DAT DEPENDENCIES...")
    print("=" * 30)
    
    dependencies = [
        "torch",
        "torchvision", 
        "transformers",
        "diffusers",
        "opencv-python",
        "moviepy",
        "pillow",
        "numpy",
        "requests",
        "pandas"
    ]
    
    for dep in dependencies:
        try:
            print(f"Dang cai dat {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], capture_output=True, text=True, check=True)
            print(f"✓ {dep} da cai dat thanh cong")
        except subprocess.CalledProcessError as e:
            print(f"✗ Loi khi cai dat {dep}: {e}")
            return False
    
    print("✓ Tat ca dependencies da duoc cai dat!")
    return True

def check_system():
    """Kiem tra he thong"""
    print("\nKIEM TRA HE THONG...")
    print("=" * 25)
    
    # Kiem tra Python
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Kiem tra PyTorch
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA not available - will use CPU")
    except ImportError:
        print("PyTorch not installed")
    
    # Kiem tra FFmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg available")
        else:
            print("FFmpeg not found")
    except FileNotFoundError:
        print("FFmpeg not found - please install manually")
    
    return True

def run_demo():
    """Chay demo"""
    print("\nCHAY DEMO TAI NGHE...")
    print("=" * 25)
    
    # Tao lenh chay
    command = [
        sys.executable, "main.py",
        "--mode", "demo",
        "--keywords", "wireless headphones", "bluetooth earbuds", "premium audio",
        "--product", "Premium Wireless Headphones - Model X1",
        "--duration", "75"
    ]
    
    print(f"Lenh: {' '.join(command)}")
    print("Dang chay... (co the mat 10-15 phut)")
    
    try:
        # Chay pipeline
        result = subprocess.run(command, cwd=Path.cwd(), 
                              text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✓ Demo chay thanh cong!")
            print("Kiem tra thu muc outputs/ de xem ket qua")
            return True
        else:
            print("✗ Demo that bai!")
            return False
            
    except Exception as e:
        print(f"✗ Loi khi chay demo: {e}")
        return False

def main():
    """Main function"""
    print("CAI DAT VA CHAY DEMO TAI NGHE")
    print("=" * 35)
    
    # Hoi nguoi dung
    print("Ban co muon cai dat dependencies va chay demo? (y/n)")
    choice = input("Nhap lua chon: ")
    
    if choice.lower() != 'y':
        print("Da huy.")
        return
    
    # Cai dat dependencies
    if not install_dependencies():
        print("Loi khi cai dat dependencies!")
        return
    
    # Kiem tra he thong
    check_system()
    
    # Hoi co muon chay demo khong
    print("\nBan co muon chay demo ngay bay gio? (y/n)")
    choice = input("Nhap lua chon: ")
    
    if choice.lower() == 'y':
        if run_demo():
            print("\n✓ HOAN THANH!")
            print("Kiem tra thu muc outputs/ de xem video da tao")
        else:
            print("\n✗ DEMO THAT BAI!")
            print("Vui long kiem tra loi va thu lai")
    else:
        print("\nDe chay demo sau, su dung lenh:")
        print("python main.py --mode demo --keywords 'wireless headphones' 'bluetooth earbuds' --product 'Premium Wireless Headphones' --duration 75")

if __name__ == "__main__":
    main()
