@control-up @api
Feature: API tests
  Interact with the Airport Gap API service "https://airportgap.com"

  @smoke
  Scenario: Verify Airport Count
    When I get airports list from airportgap.com service
    Then the response contains exactly 30 airports

  Scenario: Verify Specific Airports
    When I get airports list from airportgap.com service
    Then the response includes the following airports:
      | Airport Name        |
      | Akureyri Airport    |
      | St. Anthony Airport |
      | CFB Bagotville      |

  Scenario: Verify Distance Between Airports
    When I check the distance from "KIX" to "NRT" using airportgap.com service
    Then the calculated distance between these airports is greater than 400 kilometers
