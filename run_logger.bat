@echo off
chcp 65001 >nul
REM CS1237 Current Measurement Data Logger Setup and Run Script

echo ========================================
echo CS1237 Current Measurement Data Logger
echo ========================================
echo.

echo 📦 Installing required Python packages...
echo.

REM Try to install packages, first with minimal requirements
pip install pyserial

REM Check if installation was successful
if %errorlevel% neq 0 (
    echo ❌ Failed to install pyserial package
    echo Please try running as administrator or check your Python installation
    pause
    exit /b 1
)

echo ✅ pyserial installed successfully!
echo.

REM Try to install optional packages for data analysis
echo 📊 Installing optional data analysis packages...
pip install pandas matplotlib numpy
if %errorlevel% neq 0 (
    echo ⚠️ Optional packages installation failed, but data logger will still work
    echo Data analysis features may not be available
)

echo.
echo ✅ Package installation completed!
echo.

echo 🚀 Starting data logger...
echo.
echo 💡 Tips:
echo    - Press Ctrl+C to stop logging
echo    - Make sure Arduino is connected and running
echo    - Data will be saved in the 'data' folder
echo.

python data_logger.py

echo.
echo 👋 Data logging session ended
pause
