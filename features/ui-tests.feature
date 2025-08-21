@control-up @ui
Feature: UI tests
  Interact with the online store at "https://www.saucedemo.com"

  @smoke
  Scenario: Verify Inventory Items
    When I navigate to "https://www.saucedemo.com"
    And log in using the following credentials:
      | Field name | Field value   |
      | Username   | standard_user |
      | Password   | secret_sauce  |
    Then inventory page displays exactly 6 items

  Scenario: Add Item to Cart
    When I navigate to "https://www.saucedemo.com"
    And log in using the following credentials:
      | Field name | Field value   |
      | Username   | standard_user |
      | Password   | secret_sauce  |
    And add the 1st inventory item to the shopping cart
    Then the cart badge displays the number 1