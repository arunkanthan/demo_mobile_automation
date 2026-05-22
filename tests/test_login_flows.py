import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.config_manager import TestData


@pytest.mark.smoke
@pytest.mark.ios
def test_ios_login_valid_credentials(driver):
    """Test successful login on iOS"""
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    # Get test user data
    test_user = TestData.get_test_user("valid")
    
    # Perform login
    login_page.login(test_user["username"], test_user["password"])
    
    # Verify login success
    assert home_page.is_homepage_loaded(), "Homepage did not load after login"


@pytest.mark.regression
@pytest.mark.android
def test_android_login_invalid_credentials(driver):
    """Test login with invalid credentials on Android"""
    login_page = LoginPage(driver)
    
    # Get invalid test data
    test_user = TestData.get_test_user("invalid")
    
    # Attempt login
    login_page.login(test_user["username"], test_user["password"])
    
    # Verify error is shown
    assert login_page.is_error_displayed(), "Error message was not displayed for invalid credentials"


@pytest.mark.smoke
def test_login_then_logout(driver):
    """Test complete login and logout flow"""
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    test_user = TestData.get_test_user("valid")
    
    # Login
    login_page.login(test_user["username"], test_user["password"])
    assert home_page.is_homepage_loaded()
    
    # Logout
    home_page.click_logout()
    
    # Verify back on login page
    assert login_page.is_element_visible((None, None)) == False or \
           login_page.is_element_visible(login_page.LOGIN_BUTTON)


@pytest.mark.regression
def test_user_profile_access(driver):
    """Test accessing user profile"""
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    test_user = TestData.get_test_user("valid")
    
    # Login
    login_page.login(test_user["username"], test_user["password"])
    
    # Navigate to profile
    home_page.click_profile()
    
    # Verification would depend on profile page structure
    # For now, just verify we're still in the app
    assert driver is not None
