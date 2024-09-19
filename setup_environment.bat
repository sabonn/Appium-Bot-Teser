@echo off
setlocal enabledelayedexpansion

:: Detect OS (Windows-specific)
set "PYTHON_VERSION=3.11"
set "REQUIREMENTS_FILE=requirements.txt"
set "SDK_URL=https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"  :: Default to Windows URL
set "JDK_VERSION=11"

:: Define paths for .avd and .ini files
set "AVD_SOURCE_PATH=%cd%\Mobile"  :: Assuming these files are in a 'Mobile' directory in the current working directory
set "AVD_DEST_PATH=%USERPROFILE%\.android\avd"

:: Function to move .avd and .ini files
:move_avd_files
echo Moving .avd and .ini files to %AVD_DEST_PATH%...
if not exist "%AVD_DEST_PATH%" mkdir "%AVD_DEST_PATH%"
move /Y "%AVD_SOURCE_PATH%\*.avd" "%AVD_DEST_PATH%\"
move /Y "%AVD_SOURCE_PATH%\*.ini" "%AVD_DEST_PATH%\"
goto :eof

:: Install Homebrew (macOS) - Not applicable for Windows
:: Install common tools
:install_common_tools
echo Installing common tools...
:: Windows does not require additional setup for wget, curl, git, unzip - already included or available via other methods
goto :eof

:: Install Node.js and npm if not installed
:install_nodejs
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Node.js and npm...
    powershell -Command "iex (New-Object System.Net.WebClient).DownloadString('https://nodejs.org/dist/latest-v16.x/node-v16.16.0-x64.msi')"
) else (
    echo Node.js and npm are already installed
)
goto :eof

:: Install pip if not installed
:install_pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing pip...
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
    python get-pip.py
    del get-pip.py
) else (
    echo pip is already installed
)
goto :eof

:: Install JDK
:install_jdk
echo Installing JDK %JDK_VERSION%...
:: Download and install JDK
powershell -Command "Invoke-WebRequest -Uri https://download.oracle.com/java/11/latest/jdk-11_windows-x64_bin.zip -OutFile jdk-11.zip"
powershell -Command "Expand-Archive -Path jdk-11.zip -DestinationPath %ProgramFiles% -Force"
setx JAVA_HOME "%ProgramFiles%\jdk-11"
setx PATH "%PATH%;%JAVA_HOME%\bin"
goto :eof

:: Install Android SDK Command-Line Tools
:install_android_sdk
echo Installing Android SDK Command-Line Tools...
mkdir "%USERPROFILE%\AppData\Local\Android\Sdk"
powershell -Command "Invoke-WebRequest -Uri %SDK_URL% -OutFile android-sdk.zip"
powershell -Command "Expand-Archive -Path android-sdk.zip -DestinationPath %USERPROFILE%\AppData\Local\Android\Sdk -Force"
setx ANDROID_HOME "%USERPROFILE%\AppData\Local\Android\Sdk"
setx PATH "%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin;%ANDROID_HOME%\platform-tools"
echo Completing the Licenses
sdkmanager --licenses
echo Installing essential Android SDK components...
sdkmanager "platform-tools" "emulator" "platforms;android-35" "system-images;android-35;google_apis;x86_64"
goto :eof

:: Install Python 3.11 and pip
:install_python
echo Installing Python %PYTHON_VERSION%...
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -OutFile python-installer.exe"
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
goto :eof

:: Install Python packages from requirements.txt
:install_python_packages
if exist "%REQUIREMENTS_FILE%" (
    echo Installing Python packages from %REQUIREMENTS_FILE%...
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo Warning: %REQUIREMENTS_FILE% not found. Skipping Python package installation.
)
goto :eof

:: Install Appium and related tools
:install_appium
echo Installing Appium and related tools...
npm install -g appium appium-uiautomator2-driver selenium-webdriver
goto :eof

:: Main script execution
:main
:: Uncomment the following lines to enable installation steps
call :install_common_tools
call :install_nodejs
call :install_pip
call :install_jdk
call :install_android_sdk
call :move_avd_files
call :install_python
call :install_python_packages
call :install_appium

echo Setup completed successfully!
echo Please restart your terminal or command prompt to apply the changes.
goto :eof