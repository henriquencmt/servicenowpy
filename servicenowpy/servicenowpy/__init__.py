"""
servicenowpy, a library that helps you to get data from ServiceNow's Table API

Simple usage:

   >>> from servicenowpy import Client
   >>> sn_client = Client('<instance>.service-now.com', '<user>', '<pwd>')
   >>> inc_table = sn_client.table('incident')
   >>> records = inc_table.get(sysparm_fields='number,short_description')
   >>> for record in records:
   ...     print(record)
   {'number': 'INC0000060', 'short_description': 'Unable to connect to email'}
   {'number': 'INC0000009', 'short_description': 'Reset my password'}
   {'number': 'INC0009005', 'short_description': 'Need access to the common drive'}
"""

from servicenowpy.servicenow import Client, Table
from servicenowpy.exceptions import StatusCodeError