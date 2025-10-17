@echo off
echo ========================================
echo DEMO TAI NGHE VOI NGUOI MAU NAM CHAU A
echo ========================================
echo.
echo Cau hinh nguoi mau:
echo    Gioi tinh: male
echo    Do tuoi: young adult
echo    Dan toc: asian
echo    Phong cach: professional
echo    Boi canh: studio
echo    Trang phuc: casual smart
echo.
echo San pham: Premium Wireless Headphones - Model X1
echo Thoi luong: 75 giay
echo.
echo ========================================
echo CAI DAT DEPENDENCIES
echo ========================================
echo.
echo Dang cai dat cac thu vien can thiet...
pip install torch torchvision transformers diffusers opencv-python moviepy pillow numpy requests
echo.
echo ========================================
echo CHAY PIPELINE AI
echo ========================================
echo.
echo Dang tao video voi AI...
python main.py --mode demo --keywords "wireless headphones" "bluetooth earbuds" "premium audio" --product "Premium Wireless Headphones - Model X1" --duration 75
echo.
echo ========================================
echo HOAN THANH
echo ========================================
echo.
echo Kiem tra thu muc outputs/ de xem ket qua
echo.
pause
