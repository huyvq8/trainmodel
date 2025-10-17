"""
Simple Check for Required Software
"""
import subprocess
import sys
import os

def check_python():
    """Kiem tra Python"""
    print("KIEM TRA PYTHON...")
    print("=" * 20)
    
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    print(f"Python executable: {sys.executable}")
    
    if python_version.major >= 3 and python_version.minor >= 8:
        print("OK - Python version OK (3.8+)")
        return True
    else:
        print("ERROR - Python version too old (need 3.8+)")
        return False

def check_pip():
    """Kiem tra pip"""
    print("\nKIEM TRA PIP...")
    print("=" * 15)
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"OK - pip available: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("ERROR - pip not available")
        return False

def check_ffmpeg():
    """Kiem tra FFmpeg"""
    print("\nKIEM TRA FFMPEG...")
    print("=" * 18)
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, check=True)
        print("OK - FFmpeg available")
        version_line = result.stdout.split('\n')[0]
        print(f"  {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR - FFmpeg not found")
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
            print(f"OK - {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"MISSING - {package}")
    
    print(f"\nTong ket:")
    print(f"  Da cai dat: {len(installed_packages)}/{len(required_packages)}")
    print(f"  Con thieu: {len(missing_packages)}")
    
    if missing_packages:
        print(f"  Cac goi con thieu: {', '.join(missing_packages)}")
    
    return len(missing_packages) == 0, missing_packages

def install_packages(packages):
    """Cai dat cac goi"""
    print(f"\nCAI DAT CAC GOI...")
    print("=" * 20)
    
    for package in packages:
        try:
            print(f"Dang cai dat {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, check=True)
            print(f"OK - {package} da cai dat")
        except subprocess.CalledProcessError as e:
            print(f"ERROR - Loi khi cai dat {package}")
            return False
    
    print("OK - Tat ca cac goi da duoc cai dat!")
    return True

def main():
    """Main function"""
    print("KIEM TRA PHAN MEM CAN THIET")
    print("=" * 30)
    
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
    
    print(f"\nTONG KET:")
    print("=" * 10)
    
    if all_ok:
        print("OK - Tat ca phan mem da san sang!")
        print("Ban co the chay demo:")
        print("  python main.py --mode demo")
    else:
        print("ERROR - Con thieu mot so phan mem")
        print("\nDe cai dat cac goi Python con thieu:")
        print("  pip install torch torchvision transformers diffusers opencv-python moviepy pillow numpy requests pandas")
        print("\nHoac chay:")
        print("  python install_and_run.py")

if __name__ == "__main__":
    main()
