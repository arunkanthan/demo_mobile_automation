import pytest
from pytest_bdd import given, when, then
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.fixture
def login_page(driver):
    """Fixture for login page"""
    return LoginPage(driver)


@pytest.fixture
def home_page(driver):
    """Fixture for home page"""
    return HomePage(driver)


# Given Steps (Preconditions)
@given("the user is on the login page")
def user_on_login_page(driver):
    """Navigate to login page - adjust URL/app state as needed"""
    # In a real scenario, you'd navigate or ensure the app starts on login page
    pass


# When Steps (Actions)
@when("the user enters <username> and <password>")
def user_enters_credentials(login_page, username, password):
    """User enters username and password"""
    login_page.enter_username(username)
    login_page.enter_password(password)


@when("the user clicks the login button")
def user_clicks_login(login_page):
    """User clicks login button"""
    login_page.click_login()


@when("the user logs in with <username> and <password>")
def user_logs_in(login_page, username, password):
    """User completes login"""
    login_page.login(username, password)


# Then Steps (Assertions/Verifications)
@then("the user should be logged in successfully")
def user_logged_in_successfully(home_page):
    """Verify user is logged in"""
    assert home_page.is_homepage_loaded(), "Homepage did not load after login"


@then("an error message should be displayed")
def error_message_displayed(login_page):
    """Verify error message is shown"""
    assert login_page.is_error_displayed(), "Error message was not displayed"


@then("the error message should contain <message_text>")
def error_message_contains_text(login_page, message_text):
    """Verify error message content"""
    error_msg = login_page.get_error_message()
    assert message_text in error_msg, f"Expected '{message_text}' in error message, got '{error_msg}'"


@then("the welcome message should display")
def welcome_message_displays(home_page):
    """Verify welcome message is displayed"""
    welcome = home_page.get_welcome_message()
    assert welcome, "Welcome message was not found"
