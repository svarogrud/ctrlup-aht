from logging import getLogger
from typing import AnyStr
from urllib.parse import urlunparse, urlparse

import requests

from services.airportgap_api import AirportGapApi
from services.any_other_service_api import AnyOtherServiceApi
from utils.config import Config

logger = getLogger(__name__)


class ApiCRUD:
    """Base class for CRUD API operations."""

    def __init__(self,
                 service_config: dict,
                 session: requests.Session = None):
        self.access_token = service_config.get('token')
        self.service_url = urlparse(service_config['service_url'])
        self.session = requests.Session()

    @property
    def headers(self):
        """Return headers for API requests."""
        headers = {}
        if self.access_token:
            headers['Authorization'] = self.access_token
        return headers

    def post(self,
             url: str,
             body: dict = None,
             query: str = None,
             **kwargs) -> requests.Response:
        """Create a new resource."""
        return self.session.post(self._build_api_url(url, query=query), json=body, headers=self.headers)

    def get(self,
            url,
            query: str = None,
            **kwargs) -> requests.Response:
        """Read a resource."""
        return self.session.get(self._build_api_url(url, query=query), headers=self.headers)

    def put(self,
            **kwargs) -> requests.Response:
        """Update a resource."""
        raise NotImplementedError("Put method not implemented")

    def patch(self,
              **kwargs) -> requests.Response:
        """Update a resource."""
        raise NotImplementedError("Patch method not implemented")

    def delete(self,
               **kwargs) -> requests.Response:
        """Delete a resource."""
        raise NotImplementedError("Delete method not implemented")

    def _build_api_url(self,
                       path: str,
                       params: str = "",
                       query: str = "",
                       fragment: str = "") -> AnyStr:
        """Build a url for making API requests.
        :param path: a string to describe the path of the resource.
        :param params: parameters for last path element
        :param query: query component
        :param fragment: fragment identifier
        :return: a valid API url
        """
        return urlunparse((self.service_url.scheme, self.service_url.netloc, path, params, query, fragment))


class Api:

    def __init__(self, config: Config):
        self.config = config
        self.__airport_gap_api = None
        self.__any_other_service_api = None

    @property
    def airport_gap(self):
        """Return airport_gap API instance."""
        if not self.__airport_gap_api:
            self.__airport_gap_api = AirportGapApi(ApiCRUD(self.config.airportgap_data))
        return self.__airport_gap_api

    @property
    def any_other_service_api(self):
        """Return some other API instance."""
        if not self.__any_other_service_api:
            self.__any_other_service_api = AnyOtherServiceApi(self.crud_api)
        return self.__any_other_service_api
