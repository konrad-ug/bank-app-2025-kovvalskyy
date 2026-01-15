Feature: Transfers

Scenario: Incoming transfer increases balance
    Given Account registry is empty
    And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
    When I make "incoming" transfer of "500" to account with pesel: "90010112345"
    Then Account with pesel "90010112345" has "balance" equal to "500"

Scenario: Outgoing transfer decreases balance
    Given Account registry is empty
    And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
    And I make "incoming" transfer of "500" to account with pesel: "90010112345"
    When I make "outgoing" transfer of "200" to account with pesel: "90010112345"
    Then Account with pesel "90010112345" has "balance" equal to "300"

Scenario: Express transfer decreases balance and returns 200
    Given Account registry is empty
    And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
    And I make "incoming" transfer of "500" to account with pesel: "90010112345"
    When I make "express" transfer of "200" to account with pesel: "90010112345"
    Then Last response status code equals: "200"
    And Account with pesel "90010112345" has "balance" equal to "299"

Scenario: Unknown transfer type returns 400
    Given Account registry is empty
    And I create an account using name: "jan", last name: "kowalski", pesel: "90010112345"
    When I make "weirdtype" transfer of "100" to account with pesel: "90010112345"
    Then Last response status code equals: "400"

Scenario: Transfer for non existing account returns 404
    Given Account registry is empty
    When I make "incoming" transfer of "100" to account with pesel: "99999999999"
    Then Last response status code equals: "404"