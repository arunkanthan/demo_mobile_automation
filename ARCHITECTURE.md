# Architecture & Integration Guide

## Framework Architecture

```
demo_mobile_automation/
│
├── conftest.py              # Root Pytest configuration + BDD + Fixtures
├── pytest.ini               # Pytest settings and markers
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
│
├── config/                  # Configuration layer
│   ├── appium_config.py     # Appium server settings
│   └── capabilities.py      # Device capabilities (iOS/Android)
│
├── pages/                   # Page Object Model (POM)
│   ├── base_page.py         # Common methods for all pages
│   ├── login_page.py        # Login page
│   └── home_page.py         # Home page
│
├── steps/                   # BDD Step Definitions (pytest-bdd)
│   └── step_definitions.py  # Given/When/Then implementations
│
├── features/                # BDD Feature Files (Gherkin)
│   ├── login.feature        # Login scenarios
│   └── navigation.feature   # Navigation scenarios
│
├── tests/                   # Traditional Pytest Tests
│   ├── conftest_bdd.py      # BDD configuration
│   ├── conftest_main.py     # Main test configuration
│   └── test_login_flows.py  # Test cases
│
├── utils/                   # Utility modules
│   ├── app_utils.py         # Screenshots, waits, logging
│   └── config_manager.py    # Configuration and test data
│
├── data/                    # Test Data
│   ├── users.json           # User credentials
│   └── app_config.json      # App configuration
│
└── reports/                 # Test Reports
    ├── allure-results/      # Allure report data
    ├── screenshots/         # Failure screenshots
    └── logs/                # Test execution logs
```

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Test Framework** | Pytest | 7.4.3 |
| **BDD Framework** | pytest-bdd | 6.1.1 |
| **Mobile Automation** | Appium | 2.0+ |
| **Appium Python Client** | appium-python-client | 2.10.1 |
| **WebDriver** | Selenium | 4.14.0 |
| **Reporting** | Allure | 2.13.2 |
| **Parallelization** | pytest-xdist | 3.4.0 |
| **Language** | Python | 3.8+ |

## Integration Flow

### 1. Test Execution Flow

```
User runs pytest command
    ↓
conftest.py loads (pytest plugins)
    ↓
pytest-bdd plugin activated
    ↓
Environment variables loaded (.env)
    ↓
Driver fixture created (Appium connection)
    ↓
Tests/Features executed
    ├── BDD Features (features/*.feature)
    │   └── Matched with steps/step_definitions.py
    └── Pytest Tests (tests/test_*.py)
        └── Direct test case execution
    ↓
Screenshots taken on failure
    ↓
Driver closed & cleanup
    ↓
Reports generated (allure-results/)
```

### 2. Driver Initialization

```python
# conftest.py fixture flow
@pytest.fixture(scope="function")
def driver(request):
    # 1. Get platform from --platform argument
    platform = request.config.getoption("--platform", "ios")
    
    # 2. Load capabilities from config/capabilities.py
    if platform == "ios":
        caps = ios_capabilities()  # Reads from .env
    else:
        caps = android_capabilities()  # Reads from .env
    
    # 3. Connect to Appium server
    driver = webdriver.Remote(APPIUM_SERVER_URL, caps)
    
    # 4. Return to test
    yield driver
    
    # 5. Cleanup
    driver.quit()
```

### 3. BDD Execution Flow

```
Feature File (login.feature)
    ↓
Gherkin Scenario parsed
    ↓
Step matching
    ├── Given → step_definitions.py @given function
    ├── When → step_definitions.py @when function
    └── Then → step_definitions.py @then function
    ↓
Page Object called
    ├── LoginPage methods
    │   (login, enter_username, etc.)
    └── Appium driver interactions
    ↓
Assertions verified
    ↓
Result recorded
```

## Key Design Patterns

### 1. Page Object Model (POM)

**Purpose**: Separate test logic from UI interactions

```python
# pages/login_page.py
class LoginPage(BasePage):
    USERNAME = (AppiumBy.ID, "username")
    
    def login(self, username, password):
        self.send_text(self.USERNAME, username)
        # ... more interactions

# tests/test_login.py
def test_login(driver):
    page = LoginPage(driver)
    page.login("user", "pass")  # Clean, readable
```

### 2. Fixture Pattern

**Purpose**: Reusable test setup and teardown

```python
# conftest.py
@pytest.fixture
def driver(request):
    # Setup
    driver = initialize_appium_driver()
    yield driver
    # Teardown
    driver.quit()

# test_*.py
def test_something(driver):
    # driver automatically provided
    pass
```

### 3. Configuration Management

**Purpose**: Environment-specific settings

```python
# .env
iOS_APP_PATH=/path/to/app

# config/capabilities.py
def ios_capabilities():
    caps = {
        "app": os.getenv("iOS_APP_PATH")
    }

# Any test file
from config.capabilities import ios_capabilities
```

## Running Different Test Types

### Pytest Tests Only
```bash
# Skip BDD features, run pytest tests
pytest tests/ -v
```

### BDD Features Only
```bash
# Run only feature files
pytest features/ -v
```

### Combined (Default)
```bash
# Runs both tests/ and features/
pytest -v
```

### Platform-Specific
```bash
# iOS only
pytest --platform=ios -v

# Android only
pytest --platform=android -v
```

### Markers
```bash
# Smoke tests
pytest -m smoke -v

# iOS smoke tests
pytest -m "ios and smoke" -v

# Exclude Android tests
pytest -m "not android" -v
```

## Configuration Resolution Order

When Pytest runs, configuration is resolved in this order:

1. **Command Line Arguments**
   ```bash
   pytest --platform=ios
   ```

2. **Environment Variables (.env file)**
   ```env
   iOS_APP_PATH=/path/to/app
   ```

3. **conftest.py Fixtures**
   ```python
   @pytest.fixture
   def driver(request):
       # Uses platform from #1, settings from #2
   ```

4. **Config Files**
   ```python
   # config/capabilities.py
   # config/appium_config.py
   ```

5. **Hardcoded Defaults**
   ```python
   platform = request.config.getoption("--platform", "ios")  # Default: ios
   ```

## Parallel Execution

Run tests in parallel using pytest-xdist:

```bash
# Auto-detect CPU cores
pytest -n auto

# Use specific number of workers
pytest -n 4

# Combine with platform specification
pytest --platform=ios -n 2

# With markers
pytest -m smoke -n auto
```

**Note**: Each parallel instance gets its own driver fixture, so ensure:
- Multiple Appium servers (different ports), OR
- All tests on same platform, OR
- Appium can handle concurrent connections

## Continuous Integration

### GitHub Actions Example

```yaml
name: Mobile Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - run: npm install -g appium
      - run: appium driver install xcuitest
      
      - run: pip install -r requirements.txt
      - run: appium &
      - run: sleep 5
      
      - run: pytest --platform=ios --alluredir=reports
      
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: reports
          path: reports/
```

## Test Reporting

### Allure Report

```bash
# Generate report
pytest --alluredir=reports/allure-results

# View report
allure serve reports/allure-results
```

### JUnit XML Report

```bash
pytest --junit-xml=reports/junit.xml
```

### Custom Reports

Create custom reporting in `conftest.py`:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Custom logic here
```

## Debugging

### Enable Verbose Output
```bash
pytest -vv --tb=long
```

### Show Print Statements
```bash
pytest -s
```

### Stop on First Failure
```bash
pytest -x
```

### Drop into Debugger
```python
# In test code
import pdb; pdb.set_trace()

# Or use pytest
pytest --pdb
```

## Troubleshooting Integration

### Issue: BDD steps not found
**Solution**: Ensure `pytest_plugins = ["pytest_bdd.plugin"]` in conftest.py

### Issue: Driver not initialized
**Solution**: Check Appium server is running on correct port

### Issue: Environment variables not loading
**Solution**: Verify .env exists and is in project root

### Issue: Screenshots not saving
**Solution**: Ensure `reports/screenshots/` directory exists

## Best Practices Integration

1. **Always use Page Objects** for UI interactions
2. **Keep steps simple** - complex logic in page objects
3. **Use markers** for test categorization
4. **Separate test data** from test code
5. **Log everything** - helps debugging failures
6. **Take screenshots on failure** - configured in conftest.py
7. **Use fixtures** for common setup/teardown
8. **Run tests in isolation** - each test independent

## Next Steps

1. Configure `.env` with your device settings
2. Start Appium: `appium`
3. Run tests: `pytest -v`
4. View report: `allure serve reports/allure-results`
