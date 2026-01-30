Feature: User Authentication
  As a user I want to login and register

  Scenario: Successful login
    Given a user "admin" with password "admin123" exists
    When I login with username "admin" and password "admin123"
    Then I should receive a valid token

  Scenario: Failed login with wrong password
    Given a user "admin" with password "admin123" exists
    When I login with username "admin" and password "wrongpass"
    Then I should get an authentication error

  Scenario: Register new user
    When I register with username "newuser123" and password "securepass"
    Then the user should be created
    And I should receive a valid token

  Scenario: Cannot register duplicate username
    Given a user "existinguser" with password "pass123" exists
    When I register with username "existinguser" and password "newpass"
    Then I should get a registration error