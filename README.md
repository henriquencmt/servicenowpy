ServiceNowPy
============

A library that helps you to get data from ServiceNow's Table API.

Installation
------------

$ pip install servicenowpy

Simple usage
------------

How to retrieve data from incident table with this lib:

```python
>>> from servicenowpy import Client
>>> sn_client = Client('<instance>.service-now.com', '<user>', '<pwd>')
>>> inc_table = sn_client.table('incident')
>>> records = inc_table.get(sysparm_fields='number,short_description')
>>> for record in records:
...     print(record)
{'number': 'INC0000060', 'short_description': 'Unable to connect to email'}
{'number': 'INC0000009', 'short_description': 'Reset my password'}
{'number': 'INC0009005', 'short_description': 'Need access to the common drive'}
```

run $ docker-compose up -d

then run $ docker exec -it servicenowpy bash

to run the tests, run $ python3 -m unittest

to play with this lib, run $ python3, then start using it