from logging import getLogger

from pytest_bdd import when, then, parsers

from utils.apis import Api
from utils.result import Result

log = getLogger(__name__)


@when(parsers.re('I get airports list from airportgap.com service'), target_fixture='airports_list')
def step_get_airports(api: Api):
    result: Result = api.airport_gap.get_airports()
    assert result.success, result.error_msg
    return result.data


@then(parsers.parse('the response contains exactly {airports_num:d} airports'))
def step_check_airports_count(api: Api, airports_num: int, airports_list: list):
    assert len(airports_list) == airports_num, (
        f'Expected {airports_num} airports, but found {len(airports_list)}'
    )


@then(parsers.re('the response includes the following airports:'))
def step_check_airports_count(api: Api, datatable: list, airports_list: list):
    expected_airports = {row[0] for row in datatable[1:]}
    actual_airports = {airport['attributes']['name'] for airport in airports_list}
    assert expected_airports.issubset(actual_airports), (
        f'Mismatch in airports. Expected: {expected_airports}, Actual: {actual_airports}'
    )


@when(parsers.parse('I check the distance from "{from_airport}" to "{to_airport}" using airportgap.com service'),
      target_fixture='airports_distance')
def step_get_airports_distance(api: Api, from_airport: str, to_airport: str):
    result: Result = api.airport_gap.get_airports_distance(from_airport_iata=from_airport, to_airport_iata=to_airport)
    assert result.success, result.error_msg
    return result.data


@then(parsers.re('the calculated distance between these airports is'
                 ' (?P<comparison>greater than|less than|equal to|not equal to)'
                 ' (?P<exp_distance>.+) (?P<metric>kilometers|miles|nautical_miles)'))
def step_check_airports_distance(api: Api, comparison: str, exp_distance: int, metric: str, airports_distance: dict):
    expected_distance = float(exp_distance)
    actual_distance = airports_distance['attributes'][metric]
    if comparison == 'greater than':
        success = actual_distance > expected_distance
    elif comparison == 'less than':
        success = actual_distance < expected_distance
    elif comparison == 'equal to':
        success = actual_distance == expected_distance
    else:
        # not equal comparison
        success = actual_distance == expected_distance
    assert success, f'Expected distance to be {comparison} {expected_distance} {metric}, but got {actual_distance}'
