# JSJ
JavaScript QoL for JSON in python.
## Motivation
Being familiar with Python and with JavaScript, there was something that I just couldn't get over with JavaScript that python just doesn't have, dot notation for json. This library seeks to solve python json issues in a variety of domains.
## Basic Usage
```python
from jsj import *

url = "https://api.weather.gov/points/39.7632,-101.6483"

data = fetch(url) \
    .json() \
    .get_data()

assert data.properties.timeZone == "America/Chicago"
```

## Requesting and flattening JSON
JSJ can flatten JSON documents, just like the `pandas.normalize_json()` function.
```python
from jsj import *
# Some sample data
data = JSON([
    {
        "id": 1,
        "name": "Cole Volk",
        "fitness": {"height": 130, "weight": 60},
    },
    {"name": "Mark Reg", "fitness": {"height": 130, "weight": 60}},
    {
        "id": 2,
        "name": "Faye Raker",
        "fitness": {"height": 130, "weight": 60},
    },
])

data_flattened, keys = data.flatten()

assert data_flattened[0] == {
    "id": 1,
    "name": "Cole Volk",
    "fitness_height": 130,
    "fitness_weight": 60,
}
```

## Getting the albums released by an artist
```python
# Sets the URLs `artist` parameter to Post Malone
url = "https://musicbrainz.org/ws/2/release?artist=b1e26560-60e5-4236-bbdb-9aa5a8d5ee19&type=album|ep&fmt=json"
# Fetches, flattens and gets the titles to all releases
albums = fetch(url) \
    .json() \
    .then(lambda data: data.flatten(base=["releases"])[0]) \
    .then(lambda data: [item.title for item in data]) \
    .get_data()

assert {"Stoney", "Hollywood’s Bleeding", "beerbongs & bentleys"}.issubset(albums)
```

## Installation
This package is available on pip
```
pip install jsj
```
