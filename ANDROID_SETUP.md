# Android Minimal Setup (without Android Studio)

This file explains how to install the Android SDK components and setup an emulator without installing Android Studio.

Prerequisites
- Java JDK 11+ (OpenJDK recommended)
- Homebrew (optional, for macOS convenience)
- `sdkmanager` and `avdmanager` (provided by Android command-line tools)

Quick steps (macOS)

```bash
# install openjdk
brew install openjdk

# install Android command line tools (if you prefer not to install Android Studio)
brew install --cask android-commandlinetools

# ensure sdk manager is on PATH (adjust SDK root if needed)
export ANDROID_SDK_ROOT="$HOME/Library/Android/sdk"
export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$PATH"

# accept licenses and install components
sdkmanager --sdk_root="$ANDROID_SDK_ROOT" --licenses
sdkmanager --sdk_root="$ANDROID_SDK_ROOT" "platform-tools" "emulator" "platforms;android-33" "system-images;android-33;google_apis;x86_64"

# create an AVD
avdmanager create avd -n test_avd -k "system-images;android-33;google_apis;x86_64" --device "pixel"

# start emulator
$ANDROID_SDK_ROOT/emulator/emulator -avd test_avd &

# verify device
adb devices
```

Using the helper script

Run the included helper script which performs common steps (requires `sdkmanager` and `avdmanager`):

```bash
scripts/android_setup.sh [avd_name]
```

Notes
- You can avoid installing the emulator if you only run tests on physical devices.
- For CI or cloud device farms, use services like Firebase Test Lab, BrowserStack, or Sauce Labs.
