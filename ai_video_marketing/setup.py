"""
Setup script for AI Video Marketing System
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_cuda():
    """Check CUDA availability"""
    print("🔍 Checking CUDA availability...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA is available: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  CUDA not available, will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet, will check after installation")
        return False

def install_ffmpeg():
    """Install FFmpeg based on platform"""
    print("🎬 Installing FFmpeg...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("📥 Please download FFmpeg from: https://ffmpeg.org/download.html")
        print("   Add FFmpeg to your PATH environment variable")
        return True
    elif system == "linux":
        return run_command("sudo apt update && sudo apt install -y ffmpeg", "Installing FFmpeg on Linux")
    elif system == "darwin":  # macOS
        return run_command("brew install ffmpeg", "Installing FFmpeg on macOS")
    else:
        print(f"⚠️  Unsupported platform: {system}")
        return False

def create_virtual_environment():
    """Create virtual environment"""
    print("📦 Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Activate virtual environment"""
    print("🔧 Activating virtual environment...")
    
    system = platform.system().lower()
    if system == "windows":
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"💡 To activate virtual environment, run: {activate_script}")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📚 Installing Python packages...")
    
    # Determine pip command based on platform
    system = platform.system().lower()
    if system == "windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements")

def create_env_file():
    """Create .env file template"""
    print("🔑 Creating .env file template...")
    
    env_content = """# AI Video Marketing System - Environment Variables
# Copy this file and fill in your actual API keys

# OpenAI API Key (required for content analysis and script generation)
OPENAI_API_KEY=your_openai_api_key_here

# YouTube API Key (optional, for trend analysis)
YOUTUBE_API_KEY=your_youtube_api_key_here

# TikTok API Key (optional, for trend analysis)
TIKTOK_API_KEY=your_tiktok_api_key_here

# Other settings
LOG_LEVEL=INFO
MAX_VIDEOS_PER_KEYWORD=50
DEFAULT_VIDEO_DURATION=60
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your API keys")
    else:
        print("✅ .env file already exists")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "data",
        "models", 
        "outputs",
        "data/background_music",
        "data/logo",
        "outputs/trend_analysis",
        "outputs/content_analysis",
        "outputs/model_images",
        "outputs/scripts",
        "outputs/videos",
        "outputs/short_clips"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ All directories created")
    return True

def download_sample_assets():
    """Download sample assets"""
    print("🎵 Setting up sample assets...")
    
    # Create placeholder files
    sample_files = {
        "data/background_music/README.txt": "Place your background music files here (.mp3, .wav)",
        "data/logo/README.txt": "Place your logo files here (.png, .jpg)",
        "models/README.txt": "AI models will be downloaded here automatically"
    }
    
    for file_path, content in sample_files.items():
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    print("✅ Sample assets setup completed")
    return True

def run_test():
    """Run basic system test"""
    print("🧪 Running system test...")
    
    try:
        # Test imports
        sys.path.append(str(Path(__file__).parent / "src"))
        
        from configs.config import AI_CONFIG, VIDEO_CONFIG
        print("✅ Configuration loaded successfully")
        
        # Test basic functionality
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CUDA not available, using CPU")
        
        print("✅ System test passed")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Video Marketing System Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install FFmpeg
    install_ffmpeg()
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Create directories and files
    create_directories()
    create_env_file()
    download_sample_assets()
    
    # Check CUDA
    check_cuda()
    
    # Run test
    if not run_test():
        print("⚠️  System test failed, but setup completed")
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Edit .env file and add your API keys")
    print("\n3. Run demo:")
    print("   python main.py --mode demo")
    print("\n4. Run with custom keywords:")
    print("   python main.py --mode custom --keywords 'cooking tips' 'healthy recipes'")
    print("\n📚 Read README.md for detailed usage instructions")
    print("\n🆘 If you encounter issues, check the troubleshooting section in README.md")

if __name__ == "__main__":
    main()

