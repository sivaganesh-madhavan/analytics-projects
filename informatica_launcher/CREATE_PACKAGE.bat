@echo off
REM Package the Informatica Launcher for distribution

echo ========================================
echo Creating Distribution Package
echo ========================================
echo.

set PACKAGE_NAME=InformaticaLauncher_Package.zip
set TEMP_DIR=InformaticaLauncher

REM Create temporary directory
if exist %TEMP_DIR% rmdir /s /q %TEMP_DIR%
mkdir %TEMP_DIR%

echo Copying files...

REM Copy essential files
copy launcher.py %TEMP_DIR%\
copy launcher.bat %TEMP_DIR%\
copy QUICK_START.bat %TEMP_DIR%\
copy config.json %TEMP_DIR%\
copy requirements.txt %TEMP_DIR%\
copy README.md %TEMP_DIR%\
copy PACKAGE_README.md %TEMP_DIR%\
copy SETUP_INSTRUCTIONS.txt %TEMP_DIR%\

REM Copy icons
copy informatica_logo.png %TEMP_DIR%\
copy optum_logo.png %TEMP_DIR%\

echo.
echo Files copied successfully!
echo.
echo NEXT STEPS:
echo 1. Zip the '%TEMP_DIR%' folder
echo 2. Share the ZIP file with your colleagues
echo 3. Recipients should extract and run QUICK_START.bat
echo.
echo The package is ready in: %TEMP_DIR%\
echo.

explorer %TEMP_DIR%

pause
