from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home Page Object"""
    
    # Locators
    WELCOME_MESSAGE = (AppiumBy.ID, "welcome_message")
    USER_PROFILE = (AppiumBy.ID, "user_profile")
    LOGOUT_BUTTON = (AppiumBy.ID, "logout_button")
    
    # iOS specific locators
    iOS_WELCOME = (AppiumBy.ACCESSIBILITY_ID, "welcome_label")
    iOS_PROFILE = (AppiumBy.ACCESSIBILITY_ID, "profile_btn")
    iOS_LOGOUT = (AppiumBy.ACCESSIBILITY_ID, "logout_btn")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_homepage_loaded(self):
        """Check if homepage is loaded"""
        return self.is_element_visible(self.WELCOME_MESSAGE)
    
    def get_welcome_message(self):
        """Get welcome message"""
        return self.get_text(self.WELCOME_MESSAGE)
    
    def click_profile(self):
        """Click on user profile"""
        self.click_element(self.USER_PROFILE)
    
    def click_logout(self):
        """Click logout button"""
        self.click_element(self.LOGOUT_BUTTON)
