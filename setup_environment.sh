#!/bin/bash

set -euo pipefail  # Exit on error, undefined var, and pipe failures

# Detect OS
OS="$(uname -s)"
PYTHON_VERSION="3.11"
REQUIREMENTS_FILE="requirements.txt"
SDK_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"  # Default to Linux URL
JDK_VERSION="11"

# Define paths for .avd and .ini files
AVD_SOURCE_PATH="$(pwd)/Mobile"  # Assuming these files are in a 'Mobile' directory in the current working directory
AVD_DEST_PATH="$HOME/.android/avd"

# Define ANDROID_SDK_ROOT
ANDROID_SDK_ROOT="$HOME/Library/Android/Sdk"  # Adjust if needed

# Function to move .avd and .ini files
move_avd_files() {
    echo "Moving .avd and .ini files to $AVD_DEST_PATH..."
    mkdir -p "$AVD_DEST_PATH"  # Create the directory if it doesn't exist
    mv "$AVD_SOURCE_PATH"/*.avd "$AVD_DEST_PATH/"
    mv "$AVD_SOURCE_PATH"/*.ini "$AVD_DEST_PATH/"
}

# Install Homebrew (macOS)
install_brew_if_needed() {
    if [[ "$OS" == "Darwin" && ! $(command -v brew) ]]; then
        echo "Installing Homebrew..."
        curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash
    fi
}

# Install common tools
install_common_tools() {
    echo "Installing common tools..."
    case "$OS" in
        Linux)
            sudo apt-get update && sudo apt-get install -y wget curl git unzip || exit 1
            ;;
        Darwin)
            brew update && brew install wget curl git unzip || exit 1
            ;;
        *)
            echo "Unsupported OS: $OS"
            exit 1
            ;;
    esac
}

# Install Node.js and npm if not installed
install_nodejs() {
    if ! command -v npm &> /dev/null; then
        echo "Installing Node.js and npm..."
        case "$OS" in
            Linux)
                sudo apt-get install -y nodejs npm || exit 1
                ;;
            Darwin)
                brew install node || exit 1
                ;;
            *)
                echo "Unsupported OS: $OS"
                exit 1
                ;;
        esac
    else
        echo "Node.js and npm are already installed"
    fi
}

# Install pip if not installed
install_pip() {
    if ! command -v pip3 &> /dev/null; then
        echo "Installing pip..."
        curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    else
        echo "pip is already installed"
    fi
}

# Install JDK
install_jdk() {
    echo "Installing JDK $JDK_VERSION..."
    case "$OS" in
        Linux)
            sudo apt-get install -y openjdk-${JDK_VERSION}-jdk || exit 1
            ;;
        Darwin)
            brew install openjdk@$JDK_VERSION || exit 1
            sudo ln -sfn "$(brew --prefix)/opt/openjdk@$JDK_VERSION/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk-$JDK_VERSION.jdk
            ;;
        *)
            echo "Unsupported OS: $OS"
            exit 1
            ;;
    esac

    # Set JAVA_HOME and update PATH
    echo "Setting up Java environment variables..."
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
    echo "export JAVA_HOME=$JAVA_HOME" >> "$HOME/.bashrc"
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> "$HOME/.bashrc"

    # Apply environment variables immediately
    export PATH=$PATH:$JAVA_HOME/bin
}

# Install Android SDK Command-Line Tools
install_android_sdk() {
    echo "Installing Android SDK Command-Line Tools..."

    # Set SDK URL based on OS
    if [[ "$OS" == "Darwin" ]]; then
        SDK_URL="https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip"
    fi

    CMD_TOOLS_DIR="$ANDROID_SDK_ROOT/cmdline-tools"

    # Download and unzip command-line tools
    echo "Downloading Android SDK Command-Line Tools..."
    mkdir -p "$CMD_TOOLS_DIR"
    wget -q --show-progress "$SDK_URL" -O /tmp/cmdline-tools.zip
    echo "Extracting Android SDK Command-Line Tools..."
    unzip -q /tmp/cmdline-tools.zip -d "$CMD_TOOLS_DIR"

    # Rename the extracted directory to 'latest'
    mv "$CMD_TOOLS_DIR/cmdline-tools" "$CMD_TOOLS_DIR/latest"

    # Clean up
    rm /tmp/cmdline-tools.zip

    # Set environment variables
    export ANDROID_HOME="$ANDROID_SDK_ROOT"
    export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

    echo "Completing the Licenses"
    sdkmanager --licenses

    echo "Installing essential Android SDK components..."
    sdkmanager "platform-tools" "emulator" "platforms;android-35" "system-images;android-35;google_apis;x86_64" || exit 1

    echo "Android SDK setup completed."
}

# Install Python 3.11 and pip
install_python() {
    echo "Installing Python $PYTHON_VERSION..."
    case "$OS" in
        Linux)
            sudo apt-get install -y "python${PYTHON_VERSION}" python3-pip || exit 1
            ;;
        Darwin)
            brew install "python@$PYTHON_VERSION" || exit 1
            ;;
        *)
            echo "Unsupported OS: $OS"
            exit 1
            ;;
    esac
}

# Install Python packages from requirements.txt
install_python_packages() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing Python packages from $REQUIREMENTS_FILE..."
        pip install -r $REQUIREMENTS_FILE || exit 1
    else
        echo "Warning: $REQUIREMENTS_FILE not found. Skipping Python package installation."
    fi
}

# Install Appium and related tools
install_appium() {
    echo "Installing Appium and related tools..."
    npm install -g appium appium-uiautomator2-driver selenium-webdriver || exit 1
}

# Main script execution
main() {
    install_brew_if_needed
    install_common_tools
    install_nodejs
    install_pip
    install_jdk
    install_android_sdk
    move_avd_files
    install_python
    install_python_packages
    install_appium

    echo "Setup completed successfully!"
    echo "Please restart your terminal or run 'source ~/.bashrc' to apply the changes."
}

main