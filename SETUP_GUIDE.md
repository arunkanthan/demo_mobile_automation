# SETUP_GUIDE.md - Detailed Setup Instructions

## Prerequisites

Before starting, ensure you have the following installed:

### General Requirements
- **Python**: 3.8 or higher
- **Node.js**: 14 or higher (for npm packages)
- **Git**: Version control

### iOS Development
- **macOS**: 10.15 or higher
- **Xcode**: Latest version (includes iOS Simulator)
- **Xcode Command Line Tools**:
  ```bash
  xcode-select --install
  ```
- **iOS SDK**: Included with Xcode

### Android Development
- **Android Studio**: Latest version
- **Android SDK**: API level 21 or higher
- **Android Emulator**: Configured and running
- **Java Development Kit (JDK)**: 11 or higher

### Appium
- **Appium Server**: 2.0 or higher
  ```bash
  npm install -g appium
  appium driver install uiautomator2  # For Android
  appium driver install xcuitest      # For iOS
  ```

## Step-by-Step Installation

### 1. Clone/Navigate to Project

```bash
cd demo_mobile_automation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### 5. iOS Configuration

#### Find Your Device UDID

```bash
# Using Xcode
xcrun xctrace list devices

# Using system_profiler
system_profiler SPUSBDataType
```

#### Configure .env for iOS

```env
iOS_AUTOMATION_NAME=XCUITest
iOS_PLATFORM_VERSION=17.0
iOS_DEVICE_NAME=iPhone 15
iOS_UDID=00008120-001234567890ABCD
iOS_APP_PATH=/Users/username/path/to/app.app
iOS_BUNDLE_ID=com.example.app
```

#### Build iOS App for Testing

```bash
# Navigate to your iOS project
cd path/to/ios/project

# Build for testing
xcodebuild -scheme YourApp -configuration Debug -derivedDataPath build \
    -destination 'generic/platform=iOS' -testOnly build

# For simulator
xcodebuild -scheme YourApp -configuration Debug -sdk iphonesimulator \
    -derivedDataPath build build-for-testing
```

### 6. Android Configuration

#### Find Connected Devices

```bash
adb devices
```

#### Configure .env for Android

```env
ANDROID_AUTOMATION_NAME=UiAutomator2
ANDROID_PLATFORM_VERSION=13.0
ANDROID_DEVICE_NAME=emulator-5554
ANDROID_APP_PATH=/Users/username/path/to/app.apk
ANDROID_APP_PACKAGE=com.example.app
ANDROID_APP_ACTIVITY=.MainActivity
ANDROID_AUTO_GRANT_PERMISSIONS=true
```

#### Build Android App for Testing

```bash
# Using Gradle
cd path/to/android/project
./gradlew assembleDebug assembleAndroidTest

# Or using Android Studio UI
# Build > Build Bundles(s) / APK(s) > Build APK(s)
```

### 7. Start Appium Server

```bash
# Terminal 1: Start Appium
appium

# You should see:
# [Appium] Welcome to Appium v2.x.x
# [Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

### 8. Run Tests

```bash
# All tests
pytest -v

# iOS only
pytest --platform=ios -v

# Android only
pytest --platform=android -v

# Smoke tests
pytest -m smoke -v

# With Allure report
pytest --alluredir=reports/allure-results -v
```

## Troubleshooting

### iOS Issues

#### Xcode Build Problems
```bash
# Clean and rebuild
xcodebuild clean -scheme YourApp
rm -rf build/

# Clear Xcode cache
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

#### WebDriver Agent Issues
```bash
# Xcode 14+ specific
defaults read com.apple.dt.Xcode IDESourceTreeDisplayNames
sudo xcode-select --reset
```

#### Device Not Found
```bash
# List connected devices
xcrun xctrace list devices

# Trust device
# On device: Settings > General > Device Management > Trust Developer
```

### Android Issues

#### Emulator Not Starting
```bash
# List available emulators
emulator -list-avds

# Start specific emulator
emulator -avd emulator_name

# Or use Android Studio GUI
```

#### ADB Connection Issues
```bash
# Kill and restart ADB
adb kill-server
adb start-server

# Connect to emulator/device
adb connect device_ip:5555

# List connected devices
adb devices
```

#### App Installation Issues
```bash
# Clear app data
adb shell pm clear com.example.app

# Uninstall app
adb uninstall com.example.app

# Reinstall app
adb install path/to/app.apk
```

### General Issues

#### Port Already in Use
```bash
# Appium default port 4723
# Change port in .env:
APPIUM_SERVER_URL=http://127.0.0.1:4724

# Find process using port
lsof -i :4723
kill -9 <PID>
```

#### Appium Connection Timeout
```bash
# Ensure Appium is running
appium

# Check network connectivity
ping 127.0.0.1

# Increase timeout in config
EXPLICIT_WAIT=30
```

## Project Configuration Files

### pytest.ini
- Test discovery settings
- Markers definition
- Allure plugin configuration

### conftest.py
- Pytest fixtures
- Driver initialization
- Common test setup/teardown

### .env
- Appium server URL
- Device configurations
- App paths and identifiers
- Timeout settings

### requirements.txt
- Python dependencies
- Version specifications

## Using Environment-Specific Configurations

Create multiple .env files for different environments:

```bash
.env.local      # Local development
.env.staging    # Staging environment
.env.production # Production environment
```

Load specific environment:

```python
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env.staging')
```

## Continuous Integration Setup

### GitHub Actions Example

Create `.github/workflows/mobile-tests.yml`:

```yaml
name: Mobile Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: appium &
      - run: pytest --platform=ios -v
```

## Common Commands Cheat Sheet

```bash
# Setup
make setup          # Initial setup
make install        # Install dependencies

# Testing
make test           # Run all tests
make test-ios       # iOS tests only
make test-android   # Android tests only
make test-smoke     # Smoke tests
make test-bdd       # BDD tests

# Reports
make allure-report  # Generate Allure report

# Development
make appium-start   # Start Appium server
make clean          # Clean artifacts
make lint           # Code quality
```

## Next Steps

1. Configure your app in `.env`
2. Start Appium server: `appium`
3. Run a test: `pytest --platform=ios -v`
4. View results: `make allure-report`

## Support & Resources

- [Appium Documentation](https://appium.io)
- [Pytest Documentation](https://docs.pytest.org)
- [Pytest-BDD Guide](https://pytest-bdd.readthedocs.io)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io)
