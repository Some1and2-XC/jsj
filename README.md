# JSJ
JavaScript QoL for JSON in python.
## Motivation
Being familiar with Python and with JavaScript, there was something that I just couldn't get over with JavaScript that python just doesn't have, dot notation for json. This library seeks to solve python json issues in a variety of domains.
## Basic Usage
```python
from jsj import *

url = "https://api.weather.gov/points/39.7632,-101.6483"

time_zone = fetch(url) \
    .json() \
    .then(lambda v: v.properies.timeZone) \
    .get_data()

assert time_zone == "America/Chicago"
```
## Installation
This package is available on pip
```
pip install jsj
```
