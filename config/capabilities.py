import os
from dotenv import load_dotenv

load_dotenv()


def ios_capabilities():
    """
    Returns iOS desired capabilities for Appium
    """
    caps = {
        "platformName": "iOS",
        "automationName": os.getenv("iOS_AUTOMATION_NAME", "XCUITest"),
        "platformVersion": os.getenv("iOS_PLATFORM_VERSION", "17.0"),
        "deviceName": os.getenv("iOS_DEVICE_NAME", "iPhone 15"),
        "app": os.getenv("iOS_APP_PATH", None),
        "bundleId": os.getenv("iOS_BUNDLE_ID", None),
        "UDID": os.getenv("iOS_UDID", None),
        "shouldUseCompactResponses": False,
        "shouldUsePrebuiltWDA": False,
        "wdaStartupRetryCount": 3,
        "wdaConnectionTimeout": 60000,
        "newCommandTimeout": 60,
    }
    # Remove None values
    return {k: v for k, v in caps.items() if v is not None}


def android_capabilities():
    """
    Returns Android desired capabilities for Appium
    """
    caps = {
        "platformName": "Android",
        "automationName": os.getenv("ANDROID_AUTOMATION_NAME", "UiAutomator2"),
        "platformVersion": os.getenv("ANDROID_PLATFORM_VERSION", "13.0"),
        "deviceName": os.getenv("ANDROID_DEVICE_NAME", "emulator-5554"),
        "app": os.getenv("ANDROID_APP_PATH", None),
        "appPackage": os.getenv("ANDROID_APP_PACKAGE", None),
        "appActivity": os.getenv("ANDROID_APP_ACTIVITY", None),
        "autoGrantPermissions": os.getenv("ANDROID_AUTO_GRANT_PERMISSIONS", "true").lower() == "true",
        "newCommandTimeout": 60,
        "connectHardwareKeyboard": False,
        "autoWebview": False,
    }
    # Remove None values
    return {k: v for k, v in caps.items() if v is not None}
