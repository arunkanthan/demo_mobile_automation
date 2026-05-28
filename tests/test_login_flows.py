import os
import time

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.config_manager import TestData


def get_current_platform(driver):
    return str(driver.capabilities.get("platformName", "")).lower()


def get_app_id(driver):
    """Return the current app identifier from driver capabilities or fallback env vars."""
    app_id = driver.capabilities.get("bundleId") or driver.capabilities.get("appPackage")
    if app_id:
        return app_id

    return (
        os.getenv("iOS_BUNDLE_ID")
        or os.getenv("ANDROID_APP_PACKAGE")
        or os.getenv("BUNDLE_ID")
        or os.getenv("APP_PACKAGE")
    )


def get_app_activity(driver):
    return (
        driver.capabilities.get("appActivity")
        or os.getenv("ANDROID_APP_ACTIVITY")
        or os.getenv("APP_ACTIVITY")
    )


def launch_app(driver, app_id, app_activity=None):
    """Launch the app using the best available method for the current platform."""
    platform = get_current_platform(driver)
    try:
        if platform == "android" and app_activity:
            driver.execute_script(
                "mobile: startActivity",
                {"appPackage": app_id, "appActivity": app_activity},
            )
        else:
            driver.activate_app(app_id)
        return True
    except Exception as primary_error:
        print(f"Primary app launch failed: {primary_error}")

        if platform == "android":
            try:
                driver.execute_script(
                    "mobile: shell",
                    {
                        "command": "monkey",
                        "args": [
                            "-p",
                            app_id,
                            "-c",
                            "android.intent.category.LAUNCHER",
                            "1",
                        ],
                        "includeStderr": True,
                        "timeout": 5000,
                    },
                )
                return True
            except Exception as fallback_error:
                print(f"Android monkey launcher fallback failed: {fallback_error}")

        raise


def restart_app(driver, wait_seconds: int = 5):
    """Restart the current app using Appium client methods available in this project."""
    app_id = get_app_id(driver)
    if not app_id:
        print(
            "WARNING: Cannot restart app because neither driver capabilities nor env vars include bundleId/appPackage."
        )
        return False

    try:
        driver.terminate_app(app_id)
    except Exception as terminate_error:
        print(f"Warning: terminate_app failed, continuing with launch attempt: {terminate_error}")

    app_activity = get_app_activity(driver)
    try:
        if launch_app(driver, app_id, app_activity):
            time.sleep(wait_seconds)
            return True
    except Exception as launch_error:
        print(f"App restart failed: {launch_error}")

    return False


@pytest.mark.smoke
@pytest.mark.ios
def test_ios_login_valid_credentials(driver):
    """Test successful login on iOS"""
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    restart_app(driver, wait_seconds=5)

    time.sleep(100)
    
    # Get test user data
    # test_user = TestData.get_test_user("valid")
    
    # Perform login
    #login_page.login(test_user["username"], test_user["password"])
    
    # Verify login success
    #assert home_page.is_homepage_loaded(), "Homepage did not load after login"


# @pytest.mark.regression
# @pytest.mark.android
# def test_android_login_invalid_credentials(driver):
#     """Test login with invalid credentials on Android"""
#     # Pause to allow app to load - replace with better wait in real tests

#     login_page = LoginPage(driver)
    
     #login_page.implicitly_wait(20)
    
    # Get invalid test data
    # test_user = TestData.get_test_user("invalid")
    
    # # Attempt login
    # login_page.login(test_user["username"], test_user["password"])
    
    # # Verify error is shown
    # assert login_page.is_error_displayed(), "Error message was not displayed for invalid credentials"


# @pytest.mark.smoke
# def test_login_then_logout(driver):
#     """Test complete login and logout flow"""
#     login_page = LoginPage(driver)
#     home_page = HomePage(driver)
    
#     test_user = TestData.get_test_user("valid")
    
#     # Login
#     login_page.login(test_user["username"], test_user["password"])
#     assert home_page.is_homepage_loaded()
    
#     # Logout
#     home_page.click_logout()
    
#     # Verify back on login page
#     assert login_page.is_element_visible((None, None)) == False or \
#            login_page.is_element_visible(login_page.LOGIN_BUTTON)


# @pytest.mark.regression
# def test_user_profile_access(driver):
#     """Test accessing user profile"""
#     login_page = LoginPage(driver)
#     home_page = HomePage(driver)
    
#     test_user = TestData.get_test_user("valid")
    
#     # Login
#     login_page.login(test_user["username"], test_user["password"])
    
#     # Navigate to profile
#     home_page.click_profile()
    
#     # Verification would depend on profile page structure
#     # For now, just verify we're still in the app
#     assert driver is not None
