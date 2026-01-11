@echo off
REM Git push script using GITHUB_TOKEN environment variable

REM Check if GITHUB_TOKEN is set
if "%GITHUB_TOKEN%"=="" (
    echo Error: GITHUB_TOKEN environment variable is not set
    echo Please set it first: set GITHUB_TOKEN=your_token_here
    exit /b 1
)

REM Get the remote URL
for /f "tokens=2" %%i in ('git remote get-url origin') do set REMOTE_URL=%%i

REM Check if URL already contains token
echo %REMOTE_URL% | findstr /C:"github.com" >nul
if errorlevel 1 (
    echo Not a GitHub repository
    exit /b 1
)

REM Construct URL with token
set TOKEN_URL=https://%GITHUB_TOKEN%@github.com/BoboBH/mpj.git

REM Push with token
git push %TOKEN_URL% %*
