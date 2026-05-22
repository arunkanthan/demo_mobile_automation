import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ScreenshotUtil:
    """Utility for taking screenshots"""
    
    @staticmethod
    def take_screenshot(driver, test_name):
        """Take screenshot and save with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/screenshots/{test_name}_{timestamp}.png"
        try:
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None


class WaitUtil:
    """Utility for wait operations"""
    
    @staticmethod
    def wait_for_seconds(seconds):
        """Wait for specified seconds"""
        time.sleep(seconds)
    
    @staticmethod
    def retry_action(action, max_retries=3, delay=1):
        """Retry an action multiple times"""
        for attempt in range(max_retries):
            try:
                return action()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(delay)


class LogUtil:
    """Utility for logging"""
    
    @staticmethod
    def setup_logging(log_level=logging.INFO):
        """Setup logging configuration"""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reports/logs/test_execution.log'),
                logging.StreamHandler()
            ]
        )
    
    @staticmethod
    def get_logger(name):
        """Get logger instance"""
        return logging.getLogger(name)
