Feature: User Login
  As a user
  I want to log in to the mobile application
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user logs in with username and password
      | username | testuser |
      | password | Pass123! |
    Then the user should be logged in successfully
    And the welcome message should display

  Scenario: Login failure with invalid credentials
    Given the user is on the login page
    When the user enters invalid_user and wrong_password
    And the user clicks the login button
    Then an error message should be displayed

  Scenario Outline: Login with multiple credentials
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then <outcome>

    Examples:
      | username | password | outcome                          |
      | user1    | pass123  | the user should be logged in successfully |
      | user2    | pass456  | the user should be logged in successfully |
      | invalid  | wrong    | an error message should be displayed      |
