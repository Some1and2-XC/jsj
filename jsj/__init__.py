import asyncio
import json
import requests

from typing import Self, Callable, Any


class JSON(dict):
    """
    JSON: a wrapper class for the default dictionary.
    Wrapping the default class allows for using dot notation to get values.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Data:
    """
    Data: Generic Data Class.
    This is used to add additional functionality to all objects returned.
    """
    def __init__(self, data):
        self.data = data

    def then(self, callback: Callable) -> Self:
        """
        Calls a callback and returns a `Data` object holding the response.
        """
        return Data(callback(self.data))

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
    url = "https://dog.ceo/api/breeds/image/random"

    v = fetch(url) \
        .json() \
        .then(lambda v: v.message)

    print(v.data)

