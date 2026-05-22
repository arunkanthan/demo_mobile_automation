import pytest
import sys
from pathlib import Path
from appium import webdriver
from config.capabilities import ios_capabilities, android_capabilities
from config.appium_config import APPIUM_SERVER_URL
from utils.app_utils import ScreenshotUtil, LogUtil

# Setup logging
LogUtil.setup_logging()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="function")
def driver(request):
    """Fixture to provide Appium driver instance"""
    platform = request.config.getoption("--platform", "ios")
    
    # Get capabilities based on platform
    if platform.lower() == "ios":
        caps = ios_capabilities()
        print(f"\n{'='*60}")
        print(f"Starting iOS Driver")
        print(f"{'='*60}\n")
    else:
        caps = android_capabilities()
        print(f"\n{'='*60}")
        print(f"Starting Android Driver")
        print(f"{'='*60}\n")
    
    # Initialize driver
    driver = webdriver.Remote(APPIUM_SERVER_URL, caps)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    print(f"\n{'='*60}")
    print(f"Closing {platform} Driver")
    print(f"{'='*60}\n")
    driver.quit()


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
        "markers", "ios: marks tests for iOS platform (requires iOS)"
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
