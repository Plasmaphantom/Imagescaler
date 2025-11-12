@echo off
setlocal EnableDelayedExpansion

:: Get the directory where the batch file is located
set "SCRIPT_DIR=%~dp0"

:: Step 1: Create virtual environment
echo Creating virtual environment...
python -m venv "%SCRIPT_DIR%venv"
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 2: Activate virtual environment
echo Activating virtual environment...
call "%SCRIPT_DIR%venv\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 3: Install dependencies (Pillow)
echo Installing Pillow...
pip install Pillow
if %ERRORLEVEL% neq 0 (
    echo Failed to install Pillow.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 4: Run the Python script
echo Running image_scaler.py...
python "%SCRIPT_DIR%image_scaler.py"
if %ERRORLEVEL% neq 0 (
    echo Failed to run image_scaler.py.
    pause
    exit /b %ERRORLEVEL%
)

:: Step 5: Deactivate virtual environment
echo Deactivating virtual environment...
call "%SCRIPT_DIR%venv\Scripts\deactivate.bat"

echo Done!
pause
exit /b 0