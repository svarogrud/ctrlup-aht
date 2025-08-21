from requests import JSONDecodeError

from utils.result import Result


class AirportGapApi:

    def __init__(self, api_crud):
        self.api = api_crud

    def get_airports(self) -> Result:
        """Get airports list.
        :return: list of airports
        """
        response = self.api.get(url='/api/airports')
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        return Result(success=response.ok,
                      data=data['data'] if response.ok else None,
                      error_msg=None if response.ok else f'Failed to get airports: {data}')

    def get_airports_distance(self, from_airport_iata: str, to_airport_iata: str) -> Result:
        """Get distance between two airports.
        :param from_airport_iata: from airport's IATA
        :param to_airport_iata: to airport's IATA
        :return: Result with distance data
        """
        response = self.api.post(url='/api/airports/distance',
                                 body={'from': from_airport_iata,
                                       'to': to_airport_iata})
        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text
        return Result(success=response.ok,
                      data=data['data'] if response.ok else None,
                      error_msg=None if response.ok else f'Failed to get airports distance: {data}')
