"""
Check and Install Required Software
Kiem tra va cai dat cac phan mem can thiet
"""
import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """Kiem tra Python"""
    print("KIEM TRA PYTHON...")
    print("=" * 20)
    
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    print(f"Python executable: {sys.executable}")
    
    if python_version.major >= 3 and python_version.minor >= 8:
        print("✓ Python version OK (3.8+)")
        return True
    else:
        print("✗ Python version too old (need 3.8+)")
        return False

def check_pip():
    """Kiem tra pip"""
    print("\nKIEM TRA PIP...")
    print("=" * 15)
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✓ pip available: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("✗ pip not available")
        return False

def check_ffmpeg():
    """Kiem tra FFmpeg"""
    print("\nKIEM TRA FFMPEG...")
    print("=" * 18)
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, check=True)
        print("✓ FFmpeg available")
        # Extract version
        version_line = result.stdout.split('\n')[0]
        print(f"  {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg not found")
        print("  Please install FFmpeg from: https://ffmpeg.org/download.html")
        return False

def check_python_packages():
    """Kiem tra cac goi Python"""
    print("\nKIEM TRA CAC GOI PYTHON...")
    print("=" * 30)
    
    required_packages = [
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
    
    installed_packages = []
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            installed_packages.append(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")
    
    print(f"\nTong ket:")
    print(f"  Da cai dat: {len(installed_packages)}/{len(required_packages)}")
    print(f"  Con thieu: {len(missing_packages)}")
    
    if missing_packages:
        print(f"  Cac goi con thieu: {', '.join(missing_packages)}")
    
    return len(missing_packages) == 0, missing_packages

def install_python_packages(packages):
    """Cai dat cac goi Python"""
    print(f"\nCAI DAT CAC GOI PYTHON...")
    print("=" * 30)
    
    for package in packages:
        try:
            print(f"Dang cai dat {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, check=True)
            print(f"✓ {package} da cai dat thanh cong")
        except subprocess.CalledProcessError as e:
            print(f"✗ Loi khi cai dat {package}: {e}")
            return False
    
    print("✓ Tat ca cac goi da duoc cai dat!")
    return True

def check_gpu():
    """Kiem tra GPU"""
    print("\nKIEM TRA GPU...")
    print("=" * 15)
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✓ CUDA GPU available: {gpu_name}")
            print(f"  VRAM: {gpu_memory:.1f} GB")
            return True
        else:
            print("⚠ CUDA not available - will use CPU (slower)")
            return False
    except ImportError:
        print("⚠ PyTorch not installed yet - cannot check GPU")
        return False

def check_system_resources():
    """Kiem tra tai nguyen he thong"""
    print("\nKIEM TRA TAI NGUYEN HE THONG...")
    print("=" * 35)
    
    try:
        import psutil
        
        # CPU
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"CPU: {cpu_count} cores, usage: {cpu_usage}%")
        
        # Memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / 1024**3
        memory_usage = memory.percent
        print(f"RAM: {memory_gb:.1f} GB total, usage: {memory_usage}%")
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_gb = disk.free / 1024**3
        print(f"Disk space: {disk_gb:.1f} GB free")
        
        # Recommendations
        print(f"\nDanh gia:")
        if memory_gb >= 32:
            print("✓ RAM: Du cho AI processing")
        elif memory_gb >= 16:
            print("⚠ RAM: Co the du nhung se cham")
        else:
            print("✗ RAM: Khong du cho AI processing")
        
        if disk_gb >= 50:
            print("✓ Disk: Du cho video processing")
        else:
            print("⚠ Disk: Co the khong du cho video processing")
        
        return True
        
    except ImportError:
        print("⚠ psutil not available - cannot check system resources")
        return False

def create_installation_script():
    """Tao script cai dat"""
    print("\nTAO SCRIPT CAI DAT...")
    print("=" * 25)
    
    script_content = '''@echo off
echo ========================================
echo CAI DAT AI VIDEO MARKETING SYSTEM
echo ========================================
echo.
echo Dang cai dat cac thu vien can thiet...
echo.

pip install torch torchvision transformers diffusers opencv-python moviepy pillow numpy requests pandas

echo.
echo ========================================
echo HOAN THANH CAI DAT
echo ========================================
echo.
echo De chay demo, su dung:
echo python main.py --mode demo
echo.
pause
'''
    
    script_file = Path("install_ai_system.bat")
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ Da tao script: {script_file}")
    return script_file

def main():
    """Main function"""
    print("KIEM TRA VA CAI DAT PHAN MEM")
    print("=" * 35)
    
    all_ok = True
    
    # Kiem tra Python
    if not check_python():
        all_ok = False
    
    # Kiem tra pip
    if not check_pip():
        all_ok = False
    
    # Kiem tra FFmpeg
    if not check_ffmpeg():
        all_ok = False
    
    # Kiem tra cac goi Python
    packages_ok, missing_packages = check_python_packages()
    if not packages_ok:
        all_ok = False
    
    # Kiem tra GPU
    check_gpu()
    
    # Kiem tra tai nguyen he thong
    check_system_resources()
    
    # Tao script cai dat
    script_file = create_installation_script()
    
    print(f"\nTONG KET:")
    print("=" * 10)
    
    if all_ok:
        print("✓ Tat ca phan mem da san sang!")
        print("Ban co the chay demo ngay bay gio:")
        print("  python main.py --mode demo")
    else:
        print("✗ Con thieu mot so phan mem")
        print("De cai dat, chay:")
        print(f"  {script_file}")
        print("Hoac:")
        print("  python install_and_run.py")
    
    print(f"\nScript cai dat: {script_file}")

if __name__ == "__main__":
    main()
