@echo off
setlocal EnableExtensions DisableDelayedExpansion

rem InfoVis installer for Blender on Windows.
rem
rem Distribution layout supported by this script:
rem   install.bat
rem   packages\infovis-*.zip
rem
rem Bonsai must already be installed and enabled in Blender.
rem
rem During development, packages may also be stored in .\releases.
rem An explicit Blender executable can be supplied as the first argument:
rem   install.bat "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

set "SCRIPT_DIR=%~dp0"
set "INFO_VIS_ZIP="
set "BLENDER_VERSION="

echo.
echo ============================================================
echo                  InfoVis Installer
echo ============================================================
echo.

call :find_packages
if not defined INFO_VIS_ZIP (
    echo [ERROR] InfoVis package was not found.
    echo.
    echo Place infovis-*.zip in one of these directories:
    echo   "%SCRIPT_DIR%packages"
    echo   "%SCRIPT_DIR%releases"
    echo.
    goto :fail
)

call :find_blender "%~1"
if not defined BLENDER_EXE (
    echo [ERROR] Blender was not found.
    echo.
    echo Install Blender 5.1 or run this installer with its full path:
    echo   install.bat "C:\Path\To\Blender\blender.exe"
    echo.
    goto :fail
)

for /f "tokens=2" %%V in ('""%BLENDER_EXE%" --version 2^>nul ^| findstr /B /C:"Blender ""') do (
    if not defined BLENDER_VERSION set "BLENDER_VERSION=%%V"
)
echo Blender: "%BLENDER_EXE%"
if defined BLENDER_VERSION echo Version: %BLENDER_VERSION%
echo InfoVis package: "%INFO_VIS_ZIP%"
echo.

tasklist /FI "IMAGENAME eq blender.exe" 2>nul | find /I "blender.exe" >nul
if not errorlevel 1 (
    echo [ERROR] Blender is currently running.
    echo Close every Blender window and run this installer again.
    echo.
    goto :fail
)

echo.
echo Installing and enabling InfoVis...
call :install_extension "%INFO_VIS_ZIP%"
if errorlevel 1 (
    echo.
    echo [ERROR] Blender could not install InfoVis.
    goto :fail
)

echo.
echo ============================================================
echo Installation completed successfully.
echo Open Blender and find InfoVis in the 3D View sidebar.
echo ============================================================
echo.
pause
exit /b 0


:find_packages
for %%D in ("%SCRIPT_DIR%packages" "%SCRIPT_DIR%releases" "%SCRIPT_DIR%") do (
    if exist "%%~D" (
        if not defined INFO_VIS_ZIP (
            for /f "delims=" %%F in ('dir /B /A-D /O-D "%%~D\infovis-*.zip" 2^>nul') do (
                if not defined INFO_VIS_ZIP set "INFO_VIS_ZIP=%%~D\%%F"
            )
        )
    )
)
exit /b 0


:find_blender
if not "%~1"=="" (
    if exist "%~1" set "BLENDER_EXE=%~f1"
    exit /b 0
)

if defined BLENDER_EXE (
    if exist "%BLENDER_EXE%" exit /b 0
    set "BLENDER_EXE="
)

for /f "delims=" %%B in ('where blender.exe 2^>nul') do (
    if not defined BLENDER_EXE set "BLENDER_EXE=%%B"
)
if defined BLENDER_EXE exit /b 0

for /f "usebackq delims=" %%B in (`powershell.exe -NoProfile -Command "$roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA) | Where-Object { $_ }; Get-ChildItem $roots -Filter blender.exe -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match 'Blender' } | Sort-Object { try { [version]$_.VersionInfo.ProductVersion } catch { [version]'0.0' } } -Descending | Select-Object -First 1 -ExpandProperty FullName"`) do (
    if not defined BLENDER_EXE set "BLENDER_EXE=%%B"
)
exit /b 0


:install_extension
if /I "%INFOVIS_INSTALL_DRY_RUN%"=="1" (
    echo [DRY RUN] "%BLENDER_EXE%" --command extension install-file -r user_default -e "%~1"
    exit /b 0
)

"%BLENDER_EXE%" --command extension install-file -r user_default -e "%~1"
exit /b %ERRORLEVEL%


:fail
echo Installation was not completed.
echo.
pause
exit /b 1
