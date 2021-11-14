Examples
========

Basic usage
-----------

The simplest piece of code you can write with servicenowpy::

    from servicenowpy import Client

    sn_client = Client('instance.service-now.com', 'user', 'password')
    inc_table = sn_client.table('incident')
    inc_records = inc_table.get()

Getting large datasets
----------------------

You can get massive datasets using servicenowpy with threads, for example::

    from concurrent.futures import ThreadPoolExecutor
    from servicenowpy import Client

    sn_client = Client('instance.service-now.com', 'user', 'password')

    def get_table_records(table_name):
            table_obj = sn_client.table(table_name)
            return table_obj.get()

    with ThreadPoolExecutor() as executor:
        inc_future = executor.submit(get_table_records, 'incident')
        ritm_future = executor.submit(get_table_records, 'sc_req_item')

        inc_records = inc_future.result()
        ritm_records = ritm_future.result()

If you are using **pandas**, for example::

    import pandas as pd

    inc_df = pd.DataFrame(inc_records)

Query params
------------

Query parameters must be passed as follows::

    records = inc_table.get(
        sysparm_fields="number,short_description",
        sysparm_display_value="true"
    )