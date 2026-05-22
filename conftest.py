import pytest
import os
import sys
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


@pytest.fixture(scope="function")
def driver(request):
    """Fixture to provide driver instance based on platform marker"""
    platform = request.config.getoption("--platform", "ios").lower()
    
    if platform == "ios":
        caps = ios_capabilities()
    else:
        caps = android_capabilities()
    
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
        if caps.get('appActivity'):
            options.app_activity = caps.get('appActivity')
        if caps.get('autoGrantPermissions') is not None:
            options.auto_grant_permissions = caps.get('autoGrantPermissions')
        if caps.get('newCommandTimeout'):
            options.new_command_timeout = caps.get('newCommandTimeout')
        
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        driver.implicitly_wait(10)
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        raise
    
    yield driver
    
    # Cleanup
    print(f"\n{'='*60}")
    print(f"Closing {platform.upper()} driver...")
    print(f"{'='*60}\n")
    
    try:
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
