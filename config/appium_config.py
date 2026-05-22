import os
from dotenv import load_dotenv

load_dotenv()

# Appium Server Configuration
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

# Timeouts (in seconds)
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 20))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))

# Appium Capabilities Defaults
CAPABILITY_DEFAULTS = {
    "automationName": os.getenv("AUTOMATION_NAME", "XCUITest"),  # iOS: XCUITest, Android: UiAutomator2
    "platformVersion": os.getenv("PLATFORM_VERSION", "17.0"),
    "deviceName": os.getenv("DEVICE_NAME", "iPhone 15"),
    "UDID": os.getenv("UDID", None),
    "bundleId": os.getenv("BUNDLE_ID", None),
    "app": os.getenv("APP_PATH", None),
}
