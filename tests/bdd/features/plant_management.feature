Feature: Plant Management
  As a user I want to manage my plants

  Scenario: Create a new plant
    Given I am logged in as "testuser"
    When I create a plant named "My Rose" with species id 1
    Then the plant should be created successfully
    And the plant water level should be 100

  Scenario: View plant list
    Given I am logged in as "testuser"
    And I have plants in my collection
    When I request my plant list
    Then I should see all my plants

  Scenario: Update plant water level
    Given I am logged in as "testuser"
    And I have a plant named "Test Plant"
    When I update the water level to 50
    Then the plant water level should be 50

  Scenario: Delete a plant
    Given I am logged in as "testuser"
    And I have a plant named "Delete Me"
    When I delete the plant
    Then the plant should not exist

  Scenario: Plant dies when water reaches zero
    Given I am logged in as "testuser"
    And I have a plant named "Dying Plant"
    When I update the water level to 0
    Then the plant should be marked as dead
