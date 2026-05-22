from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.appium_config import EXPLICIT_WAIT


class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def find_element(self, locator):
        """Find element using explicit wait"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except Exception as e:
            print(f"Element not found: {locator}")
            raise e
    
    def click_element(self, locator):
        """Click an element"""
        element = self.find_element(locator)
        element.click()
    
    def send_text(self, locator, text):
        """Send text to an element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from an element"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
    
    def tap(self, locator):
        """Tap/click an element (for touch compatibility)"""
        element = self.find_element(locator)
        self.driver.execute_script("mobile: tap", {"element": element})
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.find_element(locator))
        except:
            # For Appium, try alternative scroll
            self.driver.execute_script("mobile: swipe", {"direction": "down"})
    
    def swipe(self, direction="down"):
        """Perform swipe action"""
        size = self.driver.get_window_size()
        if direction == "down":
            self.driver.swipe(size['width'] // 2, size['height'] * 0.2, 
                            size['width'] // 2, size['height'] * 0.8)
        elif direction == "up":
            self.driver.swipe(size['width'] // 2, size['height'] * 0.8, 
                            size['width'] // 2, size['height'] * 0.2)
        elif direction == "left":
            self.driver.swipe(size['width'] * 0.8, size['height'] // 2, 
                            size['width'] * 0.2, size['height'] // 2)
        elif direction == "right":
            self.driver.swipe(size['width'] * 0.2, size['height'] // 2, 
                            size['width'] * 0.8, size['height'] // 2)
