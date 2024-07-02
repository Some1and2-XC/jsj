"""
JSJ (JS-JSON)
---
JSJ is a python library aimed at getting the JavaScript Experience of working with API's.
Specifically, making data be accessible through dot notation and having a built-in way of flattening JSON values.

Basic Usage:
    from jsj import *

    url = "https://api.weather.gov/points/39.7632,-101.6483"

    time_zone = fetch(url) \
        .json() \
        .then(lambda v: v.properies.timeZone) \
        .get_data()

    assert time_zone == "America/Chicago"
"""

import json
import requests

from typing import Self, Callable, Any


class JSON(dict):
    """
    JSON: a wrapper class for the default dictionary.
    Wrapping the default class allows for using dot notation to get values.
    """
    def __getattr__(self, key):
        if type(self[key]) is dict:
            return JSON(self[key])
        else:
            return self[key]
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def flatten(self, base: list = []) -> dict:
        """
        Function for flattening data, inspired by the pandas `pd.json_normalize()` function.
        """

        def recurs_flat(item, index="") -> dict:
            out = dict()

            if type(item) is dict or type(item) is JSON:
                for k in item:
                    out |= recurs_flat(item[k], index + k + "_")

            elif type(item) is list:
                for i, v in enumerate(item):
                    out |= recurs_flat(v, index + str(i) + "_")

            else:
                out[index[:-1]] = item # Does fancy name indexing to remove '_'

            return out

        out_lst: dict | list = self
        for k in base:
            out_lst = out_lst[k]

        assert type(out_lst) is list

        return recurs_flat(out_lst)


class Data:
    """
    Data: Generic Data Class.
    This is used to add additional functionality to all objects returned.
    """
    def __init__(self, data):
        self.data = data


    def then(self, callback: Callable) -> Self:
        """Calls a callback and returns a `Data` object holding the response."""
        return Data(callback(self.data))


    def get_data(self) -> Any:
        """Returns the internal data of the data class."""
        return self.data


    def __repr__(self) -> str:
        return str(self.data)


class Response(Data):
    """
    Response: A Generic Network Response Class.
    This is used to help with casting data to json.
    """
    def __init__(self, res: requests.Response):
        super().__init__(res)


    def json(self) -> Data(JSON[Any]):
        """
        Casts internal data to a `JSON` object.
        """
        return Data(JSON(self.data.json()))


def fetch(url: str, params: dict = {}) -> Response:
    """
    A python equivalent to javascripts `fetch()` API.
    Returns a response which has the `.json()` method.
    """
    r = requests.get(url, **params)
    return Response(r)


if __name__ == "__main__":
    url = "https://api.weather.gov/points/39.7632,-101.6483"

    time_zone = fetch(url) \
        .json() \
        .then(lambda v: v.properties.timeZone) \
        .get_data()

    print(time_zone)
    assert time_zone == "America/Chicago"
