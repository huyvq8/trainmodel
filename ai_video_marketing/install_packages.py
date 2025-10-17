"""
Install Required Packages
"""
import subprocess
import sys
import time

def install_package(package):
    """Cai dat mot goi"""
    try:
        print(f"Dang cai dat {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package
        ], capture_output=True, text=True, check=True)
        print(f"OK - {package} da cai dat thanh cong")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR - Loi khi cai dat {package}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function"""
    print("CAI DAT CAC GOI PYTHON CAN THIET")
    print("=" * 35)
    
    packages = [
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
    
    print(f"Se cai dat {len(packages)} goi:")
    for i, package in enumerate(packages, 1):
        print(f"  {i}. {package}")
    
    print(f"\nBat dau cai dat...")
    print("=" * 20)
    
    success_count = 0
    failed_packages = []
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
        
        # Nghi giua cac lan cai dat
        time.sleep(1)
    
    print(f"\nTONG KET:")
    print("=" * 10)
    print(f"Thanh cong: {success_count}/{len(packages)}")
    
    if failed_packages:
        print(f"That bai: {len(failed_packages)}")
        print(f"Cac goi that bai: {', '.join(failed_packages)}")
        print(f"\nThu cai dat lai cac goi that bai:")
        for package in failed_packages:
            print(f"  pip install {package}")
    else:
        print("OK - Tat ca cac goi da duoc cai dat thanh cong!")
        print("\nBan co the chay demo:")
        print("  python main.py --mode demo")

if __name__ == "__main__":
    main()
