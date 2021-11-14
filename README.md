servicenowpy
============

[![PyPI version](https://badge.fury.io/py/servicenowpy.svg)](http://badge.fury.io/py/servicenowpy)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/servicenowpy/)
[![Downloads](https://pepy.tech/badge/servicenowpy)](https://pepy.tech/project/servicenowpy)

A library that helps you to get data from ServiceNow's Table API.

Installation
------------

```shell
pip install servicenowpy
```

Simple usage
------------

How to retrieve records from incident table with this lib:

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
_________________

[Further Documentation](https://servicenowpy.readthedocs.io/) | [Github Repository](https://github.com/henriquencmt/servicenowpy/) | [Contributing](https://github.com/henriquencmt/servicenowpy/blob/main/CONTRIBUTING.md)
