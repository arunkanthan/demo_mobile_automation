# BDD Mobile Automation Framework

A comprehensive Behavior-Driven Development (BDD) mobile automation framework for iOS and Android using Appium and Pytest.

## Project Structure

```
demo_mobile_automation/
├── features/                  # Gherkin feature files
│   ├── login.feature         # Login scenarios
│   └── navigation.feature    # Navigation scenarios
├── steps/                    # Step definitions
│   └── step_definitions.py   # Pytest-BDD step implementations
├── pages/                    # Page Object Model
│   ├── base_page.py          # Base page with common methods
│   ├── login_page.py         # Login page object
│   └── home_page.py          # Home page object
├── config/                   # Configuration files
│   ├── appium_config.py      # Appium configuration
│   └── capabilities.py       # Device capabilities
├── utils/                    # Utility modules
│   ├── app_utils.py          # Application utilities
│   └── config_manager.py     # Configuration management
├── data/                     # Test data
│   ├── users.json            # Test user credentials
│   └── app_config.json       # App configuration
├── reports/                  # Test reports and logs
├── conftest.py              # Pytest configuration
├── pytest.ini               # Pytest settings
├── requirements.txt         # Python dependencies
└── .env.example             # Example environment variables
```

## Setup Instructions

### 1. Prerequisites

- Xcode (for iOS testing)
- Android SDK (for Android testing)
- Node.js and Appium Server installed
- Python 3.8+

### 2. Install Dependencies

```bash
# Clone or navigate to project
cd demo_mobile_automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# iOS Configuration (example)
iOS_APP_PATH=/path/to/your/app.app
iOS_BUNDLE_ID=com.example.app
iOS_DEVICE_NAME=iPhone 15
iOS_UDID=00008120-001234567890ABCD

# Android Configuration (example)
ANDROID_APP_PATH=/path/to/your/app.apk
ANDROID_APP_PACKAGE=com.example.app
ANDROID_APP_ACTIVITY=.MainActivity
```

### 4. Start Appium Server

```bash
# Start Appium server (opens on port 4723 by default)
appium
```

### 5. Running Tests

#### Run all tests
```bash
pytest
```

#### Run tests for specific platform
```bash
# iOS tests
pytest --platform=ios

# Android tests
pytest --platform=android
```

#### Run specific test markers
```bash
# Run smoke tests
pytest -m smoke

# Run iOS specific tests
pytest -m ios

# Run Android specific tests
pytest -m android
```

#### Run with detailed reporting
```bash
pytest --alluredir=reports/allure-results -v
```

#### Run with Allure report generation
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## BDD Feature Files

Feature files use Gherkin syntax for behavior-driven development:

```gherkin
Feature: Feature description
  As a [user type]
  I want to [action]
  So that [benefit]

  Scenario: Scenario description
    Given [precondition]
    When [action]
    Then [expected outcome]
```

### Examples

See `features/login.feature` and `features/navigation.feature` for example BDD scenarios.

## Page Object Model (POM)

The framework uses the Page Object Model pattern for maintainability:

- **BasePage**: Contains common methods (find_element, click, send_text, etc.)
- **LoginPage**: Login-specific page object
- **HomePage**: Home-specific page object

### Creating New Page Objects

```python
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class NewPage(BasePage):
    # Define locators
    ELEMENT_LOCATOR = (AppiumBy.ID, "element_id")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Define page actions
    def perform_action(self):
        self.click_element(self.ELEMENT_LOCATOR)
```

## Step Definitions

Step definitions connect Gherkin steps to Python code:

```python
from pytest_bdd import given, when, then

@given("precondition")
def precondition(login_page):
    pass

@when("action")
def action(login_page):
    pass

@then("outcome")
def outcome(login_page):
    pass
```

## Configuration

### Appium Configuration
Edit `config/capabilities.py` to define device capabilities for iOS and Android.

### Pytest Configuration
Edit `pytest.ini` to configure markers, plugins, and output options.

## Logging and Screenshots

- Logs: `reports/logs/test_execution.log`
- Screenshots: `reports/screenshots/`
- Test reports: `reports/allure-results/`

## Running Specific Scenarios

```bash
# Run specific feature file
pytest features/login.feature

# Run specific scenario
pytest features/login.feature:4

# Run parameterized scenarios
pytest features/login.feature -k "Multiple"
```

## Continuous Integration

To integrate with Jenkins/GitHub Actions, use:

```bash
pytest --platform=ios --alluredir=reports/allure-results -v --junit-xml=reports/test-results.xml
```

## Troubleshooting

### Common Issues

1. **Appium Server Connection Error**
   - Ensure Appium server is running (`appium` command)
   - Check APPIUM_SERVER_URL in `.env`

2. **Device Not Found**
   - For iOS: Check UDID with `xcode-select --install` and Xcode
   - For Android: Check device with `adb devices`

3. **Element Not Found**
   - Verify locators in browser/inspector tools
   - Check xpath/accessibility IDs match your app

## Best Practices

1. Keep page objects focused on UI interactions
2. Use meaningful step descriptions
3. Avoid hard-coded waits; use WebDriverWait
4. Organize tests by feature
5. Maintain test data separately
6. Use setUp/tearDown for consistent test state

## References

- [Appium Documentation](https://appium.io)
- [Pytest Documentation](https://docs.pytest.org)
- [Pytest-BDD Documentation](https://pytest-bdd.readthedocs.io)
- [Page Object Model](https://www.selenium.dev/documentation/en/guidelines_and_recommendations/encouraged_practices/encouraged_practices/)

## License

MIT
