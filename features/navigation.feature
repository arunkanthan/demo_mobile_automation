Feature: Navigation Features
  As a mobile user
  I want to navigate through the application
  So that I can access different sections

  Scenario: Swipe down to reveal more content
    Given the user is on the home page
    When the user swipes down
    Then more content should be visible

  Scenario: Navigate to profile page
    Given the user is logged in
    And the user is on the home page
    When the user clicks on their profile
    Then the profile page should be displayed

  Scenario: Logout functionality
    Given the user is logged in
    And the user is on the home page
    When the user clicks the logout button
    And the user confirms logout
    Then the user should be redirected to login page
