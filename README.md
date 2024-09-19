currently im working on uploading the AVD files(its a large folder so its a pain in the ass)

# NSO Telegram Bot UI Tester

This project is designed to test Telegram bots through a user interface using an Android emulator.

## Overview

Welcome to the NSO Telegram Bot UI Tester! This tool allows you to interact with Telegram bots in a simulated environment, enabling thorough testing and development of bot interfaces.

## Download Instructions

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

This is another reason why we recommand installing Android Studio which is up next.

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

Before running, make sure that the emulator is up via `emulator -avd NSO` and open up Telegram and make sure that there are not pop-up notifications. That may ruin the testing.
Also if you are using a different Telegram user then mine, search for my bot(NnnSssOoobot and press start).

Use these commands in order.
```
python3.11 bot.py
appium
python3.11 test.py
```
Make sure that every command has started/is running fine before starting the next one.

## Conclusion

Follow these instructions to set up your environment for the NSO Telegram Bot UI Tester. If you need further assistance or encounter any issues, please consult the project's documentation or seek help from the community.

## Dockerfile

I didn't write a Dockerfile because I want this to be as autonomous as it could, meaning AVD's, and each docker image that had an Android OS created a bunch of problems I didn't want the user to experience
