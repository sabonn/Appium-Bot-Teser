# NSO Telegram Bot UI Tester

This project is designed to test Telegram bots through a user interface using an Android emulator.

## Overview

Welcome to the NSO Telegram Bot UI Tester! This tool allows you to interact with Telegram bots in a simulated environment, enabling thorough testing and development of bot interfaces.

## Download Instructions

## AVD
`https://drive.google.com/file/d/1ZC5LlKSZww_QmvTGIh_eCwWYQkFx6xKj/view?usp=sharing`
this is a link to a Google Drive for a zip file where the AVD sits, you want to download it that it's inside the project. Otherwise, the download scripts might panic.
If you want to use your own AVD I address what is required from your new AVD in the Running section of the README.

### Using the Shell or Batch Scripts

We provide shell and batch scripts to set up the environment and install necessary tools. These scripts offer flexibility in component installation.

#### macOS and Linux
Use the `setup_environment.sh` script:
```bash
bash setup_environment.sh
```

#### Windows
Use the `setup_environment.bat` script:
```batch
setup_environment.bat
```

Both scripts allow customization by uncommenting/commenting sections to install specific components.

An important note, in the installation of the cmdline tools the commands may only run in the current instance of the terminal.
A quick fix is either only using the current instance of the terminal or running this command in another instance
```
export ANDROID_HOME="$HOME/Library/Android/Sdk"
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
```

This is another reason why we recommend installing Android Studio which is up next.

## Recommended Tools

We highly recommend using Android Studio for easier setup and management of Android Virtual Devices (AVDs). It provides a user-friendly interface for creating and running AVDs, simplifying the process compared to command-line tools.

## Additional Setup

After running the scripts or setting up Android Studio, ensure all required environment variables are correctly set up. This will help avoid configuration issues.

## Included Files

The repository contains .avd and .ini files required for the emulator in the `Mobile` folder. Place these files in the appropriate directory:

- macOS/Linux: `~/.android/avd/`
- Windows: `%USERPROFILE%\.android\avd\`

While manual placement is possible, we strongly recommend using Android Studio for managing and running AVDs for a smoother experience.

## Running

Before running, make sure that the emulator is up via `emulator -avd NSO`(or whatever name you gave your emulator) open up Telegram, and make sure that there are no pop-up notifications. That may ruin the testing, and panic the code.

Use these commands in order.
```
python3.11 bot.py
appium
python3.11 test.py
```
Ensure that every command has started/is running fine before starting the next one(to ensure that all of them are running simultaneously, use different instances of the terminal to execute them).

## Conclusion

Follow these instructions to set up your environment for the NSO Telegram Bot UI Tester. If you need any more help or encounter any issues, please consult the project's documentation or seek help from the community.

## Dockerfile

I didn't write a Dockerfile because I wanted this to be as autonomous as it could, meaning AVDs, and each docker image that had an Android OS created a bunch of problems I didn't want the user to experience
