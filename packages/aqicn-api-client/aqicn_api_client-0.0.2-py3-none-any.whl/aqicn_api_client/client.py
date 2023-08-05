import os
import requests
import json
import optparse
from .helpers import list_of_dicts_to_dict

AQICN_TOKEN = os.environ.get('AQICN_TOKEN', None)
BASE_URL = "https://api.waqi.info/"

class AqicnApiClient:
    def __init__(self, token=AQICN_TOKEN):
        self.token = token
        self.base_url = BASE_URL

    def city_data(self, city):
        url = self.base_url + "feed/" + city + "/"
        return self._request(url)

    def nearest_station(self):
        url = self.base_url + "feed/here/"
        return self._request(url)

    def station_data(self, station_name):
        info = list_of_dicts_to_dict(self.search(station_name))
        station_url = info['station']['url']
        return self.city_data(station_url)

    def station_pollution(self, station_name):
        return self.station_data(station_name)['iaqi']

    def city_pollution(self, city):
        return self.city_data(city)['iaqi']

    def city_pollution_measure(self, city, measure):
        return self.city_pollution(city)[measure]['v']

    def city_aqi(self, city):
        return self.city_data(city)['aqi']

    def station_aqi(self, station_name):
        return self.station_data(station_name)['aqi']

    def station_pollution_measure(self, station_name, measure):
        return self.station_pollution(station_name)[measure]['v']

    def search(self, keyword):
        url = self.base_url + "search/"
        params = { "keyword": keyword }
        res = self._request(url, params)
        if not any(res): raise ApiException("Unknown station")
        return res

    def _request(self, url, params={}):
        params['token'] = self.token
        response = requests.get(url, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        error_msg = 'Error on Aqicn api request.'
        content = response.json()
        if content['status'] == 'ok':
            return content['data']
        else:
            raise ApiException(content['data'], resource_url = response.url)


class ApiException(Exception):
    def __init__(self, msg, resource_url=None, status_code=None):
        self.msg = msg
        self.resource_url = resource_url
        self.status_code= status_code
