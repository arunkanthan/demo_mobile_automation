import pytest
import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
from appium import webdriver
from appium.options.common import AppiumOptions
from config.capabilities import ios_capabilities, android_capabilities
from config.appium_config import APPIUM_SERVER_URL
from utils.app_utils import ScreenshotUtil, LogUtil

# Load environment variables
load_dotenv()

# Setup logging
LogUtil.setup_logging()

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def is_app_installed_android(app_package):
    """Check if an app is installed on the Android device using adb"""
    try:
        # Find adb from SDK or PATH
        android_sdk_root = os.getenv("ANDROID_SDK_ROOT") or os.getenv("ANDROID_HOME")
        if android_sdk_root:
            adb_path = os.path.join(android_sdk_root, "platform-tools", "adb")
        else:
            adb_path = "adb"
        
        # Verify adb exists
        if not os.path.exists(adb_path) and android_sdk_root:
            print(f"Warning: adb not found at {adb_path}, falling back to system adb")
            adb_path = "adb"
        
        result = subprocess.run(
            [adb_path, "shell", "pm", "list", "packages"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return f"package:{app_package}" in result.stdout
    except Exception as e:
        print(f"Error checking app installation: {e}")
        return False


def ensure_emulator_running(timeout: int = 120) -> bool:
    """Ensure an Android emulator is running. If none are attached, try to start one.

    Returns True if a device is available, False otherwise.
    """
    try:
        android_sdk_root = os.getenv("ANDROID_SDK_ROOT") or os.getenv("ANDROID_HOME")
        if android_sdk_root:
            adb_path = os.path.join(android_sdk_root, "platform-tools", "adb")
            emulator_bin = os.path.join(android_sdk_root, "emulator", "emulator")
        else:
            adb_path = "adb"
            emulator_bin = "emulator"

        print(f"DEBUG: Using adb from: {adb_path}")
        print(f"DEBUG: adb exists: {os.path.exists(adb_path)}")

        # Check for connected devices
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
        out = result.stdout or ""
        # If any device line other than the header exists with state 'device', we're good
        for line in out.splitlines():
            if line.strip() and not line.startswith("List of devices") and "device" in line and "unauthorized" not in line:
                return True

        # No device found, attempt to start emulator
        avd_name = os.getenv("ANDROID_AVD_NAME") or os.getenv("ANDROID_DEVICE_NAME") or "test_avd"
        print(f"No emulator attached; starting AVD '{avd_name}' using {emulator_bin}")

        try:
            # Launch emulator in background
            subprocess.Popen([emulator_bin, "-avd", avd_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Failed to start emulator process: {e}")
            return False

        # Wait for device to appear
        deadline = time.time() + timeout
        while time.time() < deadline:
            time.sleep(2)
            try:
                result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
                out = result.stdout or ""
                for line in out.splitlines():
                    if line.strip() and not line.startswith("List of devices") and "device" in line and "unauthorized" not in line:
                        print("Emulator is now available")
                        return True
            except Exception:
                pass

        print("Timed out waiting for emulator to become available")
        return False
    except Exception as e:
        print(f"Error ensuring emulator running: {e}")
        return False


def install_app_android(app_path):
    """Install an Android app using adb"""
    try:
        # Find adb from SDK or PATH
        android_sdk_root = os.getenv("ANDROID_SDK_ROOT") or os.getenv("ANDROID_HOME")
        adb_path = "adb"
        if android_sdk_root:
            candidate = os.path.join(android_sdk_root, "platform-tools", "adb")
            if os.path.exists(candidate):
                adb_path = candidate
            else:
                print(f"Warning: adb not found at {candidate}, falling back to system adb")

        if not os.path.exists(app_path):
            print(f"ERROR: App file not found: {app_path}")
            return False

        print(f"Using adb: {adb_path}")
        print(f"Installing app from {app_path}...")
        result = subprocess.run(
            [adb_path, "install", "-r", app_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        if "Success" in result.stdout:
            print("App installed successfully")
            return True
        else:
            print(f"Installation output: {result.stdout}")
            if "Failure" in result.stdout:
                print(f"Installation failed: {result.stdout}")
                return False
            # If no clear success or failure, assume it worked
            return True
    except Exception as e:
        print(f"Error installing app: {e}")
        return False


def uninstall_app_android(app_package):
    """Uninstall an Android app using adb"""
    try:
        # Find adb from SDK or PATH
        android_sdk_root = os.getenv("ANDROID_SDK_ROOT") or os.getenv("ANDROID_HOME")
        adb_path = "adb"
        if android_sdk_root:
            candidate = os.path.join(android_sdk_root, "platform-tools", "adb")
            if os.path.exists(candidate):
                adb_path = candidate
            else:
                print(f"Warning: adb not found at {candidate}, falling back to system adb")
        
        print(f"Using adb: {adb_path}")
        print(f"Uninstalling app {app_package}...")
        result = subprocess.run(
            [adb_path, "uninstall", app_package],
            capture_output=True,
            text=True,
            timeout=30
        )
        if "Success" in result.stdout or "removed" in result.stdout.lower():
            print(f"App {app_package} uninstalled successfully")
            return True
        else:
            print(f"Uninstall output: {result.stdout}")
            return False
    except Exception as e:
        print(f"Error uninstalling app: {e}")
        return False


@pytest.fixture(scope="function")
def driver(request):
    """Fixture to provide driver instance based on platform marker"""
    platform = request.config.getoption("--platform", "ios").lower()
    driver = None
    app_pkg = None
    
    if platform == "ios":
        caps = ios_capabilities()
    else:
        caps = android_capabilities()

    # Validate required capabilities
    if platform == "android":
        missing_caps = []
        if not caps.get('app'):
            missing_caps.append("ANDROID_APP_PATH")

        if missing_caps:
            print(f"\n{'='*60}")
            print(f"ERROR: Missing Android capabilities!")
            print(f"Please configure in .env file:")
            for cap in missing_caps:
                print(f"  - {cap}")
            print(f"{'='*60}\n")
            raise ValueError(f"Missing required capabilities: {', '.join(missing_caps)}")

        if not caps.get('appPackage'):
            print(f"WARNING: ANDROID_APP_PACKAGE is not set. Appium will try to install and launch the APK from ANDROID_APP_PATH.")
        if not caps.get('appActivity'):
            print(f"WARNING: ANDROID_APP_ACTIVITY is not set. Appium may still launch the app if ANDROID_APP_PATH is provided.")

    # Ensure an emulator/device is running before creating the Appium session
    if platform == "android":
        if not ensure_emulator_running():
            print("Warning: emulator/device did not become available before Appium session creation")
    
    print(f"\n{'='*60}")
    print(f"Initializing {platform.upper()} driver on Appium")
    print(f"{'='*60}\n")
    
    try:
        # Create AppiumOptions from capabilities dictionary
        options = AppiumOptions()
        # Load all capabilities into options
        if caps.get('platformName'):
            options.platform_name = caps.get('platformName')
        if caps.get('automationName'):
            options.automation_name = caps.get('automationName')
        if caps.get('platformVersion'):
            options.platform_version = caps.get('platformVersion')
        if caps.get('deviceName'):
            options.device_name = caps.get('deviceName')
        if caps.get('app'):
            options.app = caps.get('app')
        if caps.get('bundleId'):
            options.bundle_id = caps.get('bundleId')
        if caps.get('UDID'):
            options.udid = caps.get('UDID')
        # Set additional Android-specific options
        if caps.get('appPackage'):
            options.app_package = caps.get('appPackage')
            app_pkg = caps.get('appPackage')
        if caps.get('appActivity'):
            options.app_activity = caps.get('appActivity')
        if caps.get('autoGrantPermissions') is not None:
            options.auto_grant_permissions = caps.get('autoGrantPermissions')
        if caps.get('newCommandTimeout'):
            options.new_command_timeout = caps.get('newCommandTimeout')
        
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        driver.implicitly_wait(10)
        
        # Install app if needed (Android only)
        if platform == "android":
            app_path = caps.get('app')
            app_pkg = caps.get('appPackage')
            
            if app_path:
                print(f"\n{'='*60}")
                print(f"Checking Android app installation...")
                print(f"App Path: {app_path}")
                print(f"App Package: {app_pkg or 'NOT SET'}")
                print(f"{'='*60}\n")
                # Ensure emulator/device is running before checking/installing
                if not ensure_emulator_running():
                    print("Warning: No emulator/device available; continuing and letting Appium handle device startup")

                if app_pkg:
                    if not is_app_installed_android(app_pkg):
                        print(f"App {app_pkg} not installed. Installing...")
                        if os.path.exists(app_path):
                            if install_app_android(app_path):
                                print(f"Successfully installed {app_pkg}")
                            else:
                                print(f"Failed to install {app_pkg}")
                        else:
                            print(f"App file not found: {app_path}")
                    else:
                        print(f"App {app_pkg} is already installed")
                else:
                    print("ANDROID_APP_PACKAGE is not set; installing APK directly from path")
                    if os.path.exists(app_path):
                        if install_app_android(app_path):
                            print("APK installed directly from ANDROID_APP_PATH")
                        else:
                            print("Failed to install APK from ANDROID_APP_PATH")
                    else:
                        print(f"App file not found: {app_path}")
        
        # Launch the app explicitly
        print(f"\n{'='*60}")
        print(f"Launching {platform.upper()} app...")
        print(f"{'='*60}\n")
        
        try:
            if platform == "android":
                app_pkg_val = caps.get('appPackage')
                app_activity = caps.get('appActivity')

                if app_pkg_val and app_activity:
                    try:
                        driver.execute_script(
                            "mobile: startActivity",
                            {"appPackage": app_pkg_val, "appActivity": app_activity}
                        )
                        print(f"Started activity {app_activity} for {app_pkg_val}")
                    except Exception as e:
                        print(f"Could not start activity {app_activity} for {app_pkg_val}: {e}")
                        print("Falling back to activate_app()")
                        try:
                            driver.activate_app(app_pkg_val)
                            print(f"App {app_pkg_val} activated")
                        except Exception as e2:
                            print(f"Could not activate app {app_pkg_val}: {e2}")
                elif app_pkg_val:
                    try:
                        driver.activate_app(app_pkg_val)
                        print(f"App {app_pkg_val} activated")
                    except Exception as e:
                        print(f"Could not activate app {app_pkg_val}: {e}")
                else:
                    print("ANDROID_APP_PACKAGE not set; cannot start Android app explicitly")
            else:
                try:
                    driver.execute_script("mobile: launchApp", {})
                    print(f"{platform.upper()} app launched via mobile: launchApp")
                except Exception as e:
                    print(f"Could not launch iOS app with mobile: launchApp: {e}")
        except Exception as e:
            print(f"App launch encountered an issue: {e}")
            # Don't fail the test setup - continue with what we have
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        raise
    
    yield driver
    
    # Cleanup
    print(f"\n{'='*60}")
    print(f"Closing {platform.upper()} driver...")
    print(f"{'='*60}\n")
    
    # Uninstall app after test (Android only)
    if platform == "android" and app_pkg:
        print(f"\n{'='*60}")
        print(f"Uninstalling app after test...")
        print(f"{'='*60}\n")
        uninstall_app_android(app_pkg)
    
    try:
        if driver:
            driver.quit()
    except Exception as e:
        print(f"Error closing driver: {e}")


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--platform",
        action="store",
        default="ios",
        help="Platform to run tests on: ios or android"
    )


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "ios: marks tests for iOS platform"
    )
    config.addinivalue_line(
        "markers", "android: marks tests for Android platform"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.failed and call.when == "call":
        # Get driver from fixtures
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                ScreenshotUtil.take_screenshot(driver, item.name)


@pytest.fixture(scope="function")
def mobile_app():
    """Fixture for mobile app instance"""
    return MobileApp()


class MobileApp:
    """Generic mobile app fixture"""
    pass
