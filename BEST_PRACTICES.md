# BEST_PRACTICES.md - Framework Best Practices

## Mobile Test Automation Best Practices

### 1. Page Object Model (POM)

#### Good Practice ✓
```python
class LoginPage(BasePage):
    USERNAME = (AppiumBy.ID, "username_field")
    PASSWORD = (AppiumBy.ID, "password_field")
    LOGIN_BTN = (AppiumBy.ID, "login_button")
    
    def login(self, username, password):
        self.send_text(self.USERNAME, username)
        self.send_text(self.PASSWORD, password)
        self.click_element(self.LOGIN_BTN)
```

#### Avoid ✗
```python
# Direct driver calls in test
def test_login(driver):
    driver.find_element(AppiumBy.ID, "username").send_keys("user")
    # ... scattered locators and actions
```

### 2. Wait Strategies

#### Good Practice ✓
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((AppiumBy.ID, "element")))
element.click()
```

#### Avoid ✗
```python
import time
time.sleep(5)  # Fixed wait - unpredictable
driver.find_element(AppiumBy.ID, "element").click()
```

### 3. Test Data Management

#### Good Practice ✓
```python
# External data file: data/users.json
{
    "valid_user": {
        "username": "testuser",
        "password": "TestPass123!"
    }
}

# In test
test_user = TestData.load_test_data("users")["valid_user"]
```

#### Avoid ✗
```python
# Hard-coded in tests
def test_login():
    login_page.login("testuser", "TestPass123!")
```

### 4. Locator Strategy

#### Priority Order (Best to Worst)
1. **Accessibility ID** (Recommended for cross-platform)
   ```python
   (AppiumBy.ACCESSIBILITY_ID, "login_button")
   ```

2. **ID** (Android: resource-id, iOS: NSAccessibility)
   ```python
   (AppiumBy.ID, "submit_btn")
   ```

3. **Class Name**
   ```python
   (AppiumBy.CLASS_NAME, "UIButton")
   ```

4. **XPath** (Last resort, fragile)
   ```python
   (AppiumBy.XPATH, "//XCUIElementTypeButton[@name='Login']")
   ```

### 5. Platform-Specific Code

#### Good Practice ✓
```python
from config.capabilities import get_platform

def get_locator(element_type):
    platform = get_platform()
    if platform == "iOS":
        return iOS_LOCATORS[element_type]
    else:
        return ANDROID_LOCATORS[element_type]
```

#### Avoid ✗
```python
# Scattered platform checks
if "iPhone" in device_name:
    element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "login")
else:
    element = driver.find_element(AppiumBy.ID, "login")
```

### 6. BDD Feature Writing

#### Good Practice ✓
```gherkin
Feature: User Authentication
  Scenario: Successful login with valid credentials
    Given the user is on the login screen
    When the user enters valid credentials
    And the user taps the login button
    Then the user should see the home screen
```

#### Avoid ✗
```gherkin
# Too technical, implementation-focused
Scenario: User login flow
    Given driver is initialized
    When find element by ID and send keys
    Then verify element visibility
```

### 7. Error Handling

#### Good Practice ✓
```python
try:
    element = self.find_element(locator)
except TimeoutException:
    self.take_screenshot("element_not_found")
    raise AssertionError(f"Element not found: {locator}")
except NoSuchElementException as e:
    logging.error(f"Element disappeared: {e}")
    raise
```

#### Avoid ✗
```python
# Bare exceptions
try:
    element = driver.find_element(AppiumBy.ID, "element")
except:
    pass
```

### 8. Logging and Debugging

#### Good Practice ✓
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Starting login flow")
logger.debug(f"Username: {username}")
logger.error("Login failed", exc_info=True)
```

#### Include in Tests
```python
# Screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if outcome.failed:
        driver.save_screenshot(f"failure_{item.name}.png")
```

### 9. Test Organization

```
tests/
├── test_login.py          # Single feature tests
├── test_navigation.py
├── test_checkout.py
├── conftest.py            # Shared fixtures
└── features/              # BDD feature files
    ├── login.feature
    └── navigation.feature
```

### 10. Performance Optimization

#### Good Practice ✓
```python
# Run tests in parallel using pytest-xdist
pytest -n auto

# Use pytest markers for test categorization
@pytest.mark.smoke
@pytest.mark.ios

# Skip expensive tests when not needed
@pytest.mark.skipif(not ios_available, reason="iOS not available")
```

### 11. CI/CD Integration

#### GitHub Actions Example
```yaml
- name: Run Mobile Tests
  run: |
    appium &
    pytest --platform=ios --alluredir=reports/allure-results
    
- name: Upload Reports
  if: always()
  uses: actions/upload-artifact@v2
  with:
    name: test-reports
    path: reports/
```

### 12. Configuration Management

#### Good Practice ✓
```python
# Use environment variables for configuration
from dotenv import load_dotenv
import os

APPIUM_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
TIMEOUT = int(os.getenv("EXPLICIT_WAIT", 20))
```

#### Avoid ✗
```python
# Hard-coded values
APPIUM_URL = "http://127.0.0.1:4723"
TIMEOUT = 20
```

## Testing Anti-Patterns to Avoid

### ❌ Flaky Tests
- Using `time.sleep()` instead of waits
- Timing-dependent assertions
- Testing multiple features in one test

### ❌ Hard-coded Data
- Test data embedded in test code
- Device-specific paths
- Hard-coded URLs

### ❌ Poor Locators
- Changing XPath dynamically
- Locators based on text that changes
- Deeply nested XPath expressions

### ❌ Lack of Error Context
- Generic error messages
- No screenshots on failure
- Missing logs

## Checklist for New Tests

- [ ] Uses Page Object Model
- [ ] Has clear, descriptive name
- [ ] Uses explicit waits
- [ ] External test data
- [ ] Proper logging
- [ ] Screenshot on failure
- [ ] Single responsibility
- [ ] Parameterized where appropriate
- [ ] Includes teardown/cleanup
- [ ] Works on both iOS and Android (if applicable)

## Code Review Checklist

- [ ] Follows POM pattern
- [ ] No hard-coded values
- [ ] Proper exception handling
- [ ] Uses appropriate waits
- [ ] Has meaningful assertions
- [ ] Includes logging
- [ ] Test is isolated and independent
- [ ] Works on target platforms
- [ ] Documentation is clear
