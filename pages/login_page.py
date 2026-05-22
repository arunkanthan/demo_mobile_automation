from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login Page Object"""
    
    # Locators
    USERNAME_FIELD = (AppiumBy.ID, "username")
    PASSWORD_FIELD = (AppiumBy.ID, "password")
    LOGIN_BUTTON = (AppiumBy.ID, "login_button")
    ERROR_MESSAGE = (AppiumBy.ID, "error_message")
    
    # iOS specific locators
    iOS_USERNAME = (AppiumBy.ACCESSIBILITY_ID, "username_textfield")
    iOS_PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "password_textfield")
    iOS_LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "login_btn")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_username(self, username):
        """Enter username"""
        self.send_text(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """Enter password"""
        self.send_text(self.PASSWORD_FIELD, password)
    
    def click_login(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
