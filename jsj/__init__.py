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
        .then(lambda v: v.properties.timeZone) \
        .get_data()

    assert time_zone == "America/Chicago"
"""

import json
import requests
from Lindex import lindex
from os import environ

from typing_extensions import Self, Callable, Any

# Environment Variable for defining dehavior of values using dot notatition not being found
JSJ_NONE_ENV_KEY = "JSJ_NONE"


class JSON(lindex):
    """
    JSON: a wrapper class for the default dictionary.
    Wrapping the default class allows for using dot notation to get values.
    If dot notation can't find the attribute, what is returned is based on the `JSJ_NONE` environment variable.

    If this environment variable is set to "err", an error will be thrown.
    If this environment variable is set to "none", the `None` value will be returned. This is the default.
    """

    _default_key = "_default_key"


    def __init__(self, data: dict | list = None):
        """Function for initializing a new JSON object"""

        if data is None: data = dict()

        if type(data) is list:
            data = {self.__class__._default_key: data}
            self._is_list = True
        else:
            self._is_list = False

        super().__init__(data)


    def __getattr__(self, key):

        # Checks environment variable if the key isn't found.
        if key not in self:
            if JSJ_NONE_ENV_KEY not in environ or environ[JSJ_NONE_ENV_KEY] == "none":
                return None
            elif environ[JSJ_NONE_ENV_KEY] == "err":
                raise AttributeError(f"Attribute '{key}' is not found!")
            else:
                raise AttributeError(
                    f"Attribute '{key}' is not found & no valid parameter set" + \
                    f"(consider changing the environment variable '{JSJ_NONE_ENV_KEY}'.)")

        if type(self[key]) is dict:
            return JSON(self[key])
        else:
            return self[key]
    __delattr__ = dict.__delitem__

    def flatten(self, base: list = None, sep: str = "_", debug: bool = False) -> (list[Self], list[Any]):
        """
        Function for flattening data, inspired by the pandas `pd.json_normalize()` function.
        Takes a `base` array of indexes and self.
        Returns a list of flatten dictionaries and a list of all the keys used.
        """

        # ensures the type of base
        if base is None: base = []
        if type(base) != list: base = [base]

        # Makes sure to look at the default key if the value passed was a list
        if self._is_list:
            base.insert(0, self.__class__._default_key)

        known_keys = []

        def recurs_flat(item, index: str = "", keys = None) -> list[Self]:
            """Internal function for recursively flattening a dictionary."""

            # Initializes out dict
            out: list[Self] = []

            # Dict logic
            if type(item) is dict or type(item) is JSON:
                # Goes through each k/v pair
                for k, v in item.items():
                    # ensures there is at least one dict in output
                    if len(out) == 0: out.append(JSON())

                    # go through each return value from recurs_flat
                    for i, entry in enumerate(recurs_flat(v, index + str(k) + sep)):

                        # if v is a list, duplicate the first entry
                        if type(v) is list:
                            out.append(out[0])

                            for e_k in entry.keys():
                                if e_k in out[-1]:
                                    del out[-1][e_k]

                            out[-1] = JSON(entry | out[-1])

                        else:
                            for out_entry, _ in enumerate(out):
                                out[out_entry] |= entry

                    if type(v) is list:
                        out = out[1::]

            # List logic
            elif type(item) is list:  # For each value in the list
                for i, v in enumerate(item):  # For each result in the recurs flat
                    for res in recurs_flat(v, index):
                        if res: out.append(res)

            # Value logic
            else:
                new_key = index[:-len(sep)]
                if new_key not in known_keys:
                    known_keys.append(new_key)

                if len(out) == 0:
                    if item:
                        out = [JSON({new_key: item})]
                    else:
                        out = []
                else:
                    out[-1][new_key] = item # Does fancy name indexing to remove '_'

            return out

        # Walks the dict to where the `base` points
        out_lst: dict | list = self
        for k in base:
            if type(out_lst) is not list and k not in out_lst:
                raise KeyError(f"Can't find key '{k}' in data! (Make sure this is a reasonable base.)")
            out_lst = out_lst[k]

        if type(out_lst) is not list:
            raise ValueError(f"Can't find array from base '{base}'!")

        # Does some basic checks
        if type(out_lst) is list: out_lst = [out_lst]
        if len(out_lst) == 0: return []

        # Gets the data and ensures the dictionaries have values in them
        out_data = recurs_flat(out_lst)
        return [v for v in out_data if v], known_keys


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


def fetch(url: str, *args, **kwargs) -> Response:
    """
    A python equivalent to javascripts `fetch()` API.
    Returns a response which has the `.json()` method.
    """
    r = requests.get(url, *args, **kwargs)
    return Response(r)


if __name__ == "__main__":
    # Weather API test
    url = "https://api.weather.gov/points/39.7632,-101.6483"

    time_zone = fetch(url) \
        .json() \
        .then(lambda v: v.properties.timeZone) \
        .get_data()

    assert time_zone == "America/Chicago"

    # MusicBrainz API test
    url = "https://musicbrainz.org/ws/2/release?artist=b1e26560-60e5-4236-bbdb-9aa5a8d5ee19&type=album|ep&fmt=json"

    albums = fetch(url) \
        .json() \
        .then(lambda data: data.flatten(base=["releases"])[0]) \
        .then(lambda data: [item.title for item in data]) \
        .get_data()

    albums = list(set(albums))
    print(albums)
