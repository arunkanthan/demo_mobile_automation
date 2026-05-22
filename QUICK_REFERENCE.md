# Quick Reference Guide

## Installation & Setup (5 minutes)

```bash
# 1. Navigate to project
cd demo_mobile_automation

# 2. Create virtual environment & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your device settings

# 4. Start Appium (separate terminal)
appium

# 5. Run tests
pytest --platform=ios -v
```

## Common Commands

### Running Tests
```bash
pytest                              # All tests
pytest -v                           # Verbose output
pytest -s                           # Show print statements
pytest -x                           # Stop on first failure
pytest -k "login"                   # Run tests matching name
pytest --platform=ios               # iOS only
pytest --platform=android           # Android only
pytest -m smoke                     # Markers
pytest features/                    # BDD features only
pytest tests/                       # Pytest tests only
pytest -n auto                      # Parallel execution
```

### Reports & Debugging
```bash
pytest --alluredir=reports/allure-results  # Generate Allure report
allure serve reports/allure-results        # View Allure report
pytest --pdb                               # Debug with pdb
pytest --lf                                # Run last failed
pytest --ff                                # Failed first
```

### Make Commands
```bash
make help                   # Show all available commands
make setup                  # Initial setup
make install                # Install dependencies
make test                   # Run all tests
make test-ios               # iOS tests
make test-android           # Android tests
make test-smoke             # Smoke tests
make test-regression        # Regression tests
make test-bdd               # BDD tests
make allure-report          # Generate & serve report
make appium-start           # Start Appium
make clean                  # Clean artifacts
```

## Configuration Quick Tips

### Update .env file
```env
# Appium Server
APPIUM_SERVER_URL=http://127.0.0.1:4723

# iOS
iOS_APP_PATH=/path/to/your/app.app
iOS_BUNDLE_ID=com.example.app
iOS_DEVICE_NAME=iPhone 15

# Android
ANDROID_APP_PATH=/path/to/your/app.apk
ANDROID_APP_PACKAGE=com.example.app
ANDROID_APP_ACTIVITY=.MainActivity
```

### Find Device Info

**iOS:**
```bash
xcrun xctrace list devices
system_profiler SPUSBDataType
```

**Android:**
```bash
adb devices
adb shell getprop ro.build.version.release
```

## Creating New Tests

### BDD Feature
1. Create `.feature` file in `features/`
2. Write Gherkin scenarios
3. Create step functions in `steps/step_definitions.py`

### Pytest Test
1. Create `test_*.py` file in `tests/`
2. Import page objects and fixtures
3. Write test functions

### Page Object
1. Create new file in `pages/`
2. Extend `BasePage`
3. Define locators as class variables
4. Create action methods

## Test Data Management

### Load from JSON
```python
from utils.config_manager import TestData

user = TestData.load_test_data("users")
```

### Create New Data File
1. Create JSON file in `data/` folder
2. Load using `TestData.load_test_data("filename")`

## Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| Appium connection timeout | Ensure Appium running: `appium` |
| Element not found | Verify locator with device inspector |
| .env not loading | Check .env exists in project root |
| Port already in use | Change port: `lsof -i :4723` then `kill -9 <PID>` |
| Tests timeout | Increase EXPLICIT_WAIT in .env |
| Screenshots not saving | Missing reports/screenshots dir |
| Device not found | Run `adb devices` or check iOS UDID |

## Project Structure Quick Reference

```
demo_mobile_automation/
├── conftest.py              ← Main configuration (don't delete!)
├── pytest.ini               ← Pytest settings
├── .env                     ← Your device settings (create from .env.example)
├── config/                  ← Appium & device capabilities
├── pages/                   ← Page objects
├── steps/                   ← BDD step definitions
├── features/                ← Gherkin feature files
├── tests/                   ← Pytest test files
├── utils/                   ← Helper utilities
├── data/                    ← Test data (JSON)
├── reports/                 ← Generated reports
├── requirements.txt         ← Python dependencies
└── README.md                ← Full documentation
```

## Essential Pytest Features

### Fixtures
```python
# Define in conftest.py
@pytest.fixture
def driver(request):
    # setup
    yield driver
    # cleanup

# Use in tests
def test_something(driver):
    pass
```

### Markers
```python
# Define in conftest.py
config.addinivalue_line("markers", "smoke: smoke tests")

# Use in tests
@pytest.mark.smoke
def test_login():
    pass

# Run specific marker
pytest -m smoke
```

### Parametrization
```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(username, password):
    pass
```

## BDD Quick Start

### Feature File Syntax
```gherkin
Feature: Feature description
  Scenario: Scenario description
    Given precondition
    When action
    Then expected outcome
    And additional verification
```

### Step Definition Syntax
```python
from pytest_bdd import given, when, then

@given("precondition")
def precondition(page_object):
    pass

@when("action")
def action(page_object):
    pass

@then("expected outcome")
def assertion(page_object):
    pass
```

## Page Object Quick Pattern

```python
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class MyPage(BasePage):
    ELEMENT = (AppiumBy.ID, "element_id")
    
    def action(self, value):
        self.send_text(self.ELEMENT, value)
```

## Parallel Execution

```bash
# Install pytest-xdist (already in requirements.txt)
pytest -n auto              # Auto detect cores
pytest -n 4                 # Use 4 workers
pytest -n 2 --platform=ios  # 2 workers, iOS
```

## CI/CD Quick Setup

### GitHub Actions
```yaml
- run: pip install -r requirements.txt
- run: appium &
- run: sleep 5
- run: pytest --platform=ios -v
```

### Jenkins
```groovy
stage('Test') {
    steps {
        sh 'pip install -r requirements.txt'
        sh 'appium &'
        sh 'sleep 5'
        sh 'pytest --platform=ios -v'
    }
}
```

## Performance Tips

1. **Use parallel execution**: `pytest -n auto`
2. **Run only needed tests**: `pytest -m smoke`
3. **Skip slow tests**: `@pytest.mark.skip`
4. **Use fixtures for setup**: Avoid repetition
5. **Optimize waits**: Use `EXPLICIT_WAIT` appropriately

## Documentation Files

- `README.md` - Overview and setup
- `SETUP_GUIDE.md` - Detailed installation
- `BEST_PRACTICES.md` - Do's and don'ts
- `ARCHITECTURE.md` - Framework design
- `QUICK_REFERENCE.md` - This file

## Getting Help

1. Check documentation files
2. Review example tests in `tests/test_login_flows.py`
3. Check example features in `features/login.feature`
4. Review page objects in `pages/`
5. Check Appium docs: https://appium.io
6. Check Pytest docs: https://docs.pytest.org

## Common Test Patterns

### Basic Test
```python
def test_login(driver):
    page = LoginPage(driver)
    page.login("user", "pass")
    assert page.is_logged_in()
```

### With Setup/Teardown
```python
@pytest.fixture
def login_required(driver):
    page = LoginPage(driver)
    page.login("user", "pass")
    yield page

def test_something(login_required):
    page = login_required
    page.do_action()
```

### Parameterized
```python
@pytest.mark.parametrize("cred", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(driver, cred):
    page = LoginPage(driver)
    page.login(cred[0], cred[1])
```

### With Markers
```python
@pytest.mark.smoke
@pytest.mark.ios
def test_login(driver):
    pass
```

## Next Steps

1. Update `.env` with your device configuration
2. Start Appium: `appium`
3. Run: `pytest --platform=ios -v`
4. Check results: `allure serve reports/allure-results`
5. View logs: `cat reports/logs/test_execution.log`
