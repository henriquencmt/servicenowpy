import json
import re
import requests

from .exceptions import StatusCodeError

class Client:
    """
    Represents a ServiceNow instance.

    Example
    -------

    import servicenowpy

    sn_client = servicenowpy.Client('https://dev01234.service-now.com', 'admin', 'secret')


    :param instance_url: ServiceNow instance URL.
    :param user: Instance user.
    :param pwd: Instance password.
    """

    def __init__(self, instance_url: str, user: str, pwd: str):
        self.__instance_url = self.make_api_url(instance_url)
        self.__credentials = user, pwd

    def make_api_url(self, instance_url):
        """Returns instance URL with '/api/now/' appended."""

        m = re.search(r'^https?://', instance_url)
        url = f'https://{instance_url}' if not m else instance_url
        url = url.rstrip('/')
        url += '/api/now/'
        return url

    def table(self, table):
        """
        Returns servicenowpy.Table object.

        :param table: The table name.
        :rtype: servicenowpy.Table
        """

        return Table(table, self.__instance_url, self.__credentials)


class Table:
    """
    Represents ServiceNow's Table API.

    Example
    -------

    from servicenowpy import Client

    sn_client = Client('https://dev01234.service-now.com', 'admin', 'secret')
    inc_table = sn_client.table('incident')
    ritm_table = sn_client.table('sc_req_item')
    
    :param table: The table name.
    :param instance_url: ServiceNow instance URL".
    :param credentials: Tuple containing user and password, respectively.
    """

    def __init__(self, table, instance_url, credentials: tuple):
        self.__table = table
        self.__instance_url = instance_url
        self.__credentials = credentials

    def get(
        self,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a GET request to the instance table.

        :param api_version: API version, if API versioning is enabled.
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        :rtype: list
        """

        url = self.make_url(api_version, **kwargs)
        if verbose:
            print(url)
        session = self.get_session(headers)

        result = []
        while url:
            response = session.get(url)
            self.check_status_code(response)

            data = response.json()
            result.extend(data['result'])

            # Searches for the next page link in the pagination relative links
            try:
                link = response.headers['Link']
                m = re.search(r'(.*),<(.*)>;rel="next', link)
                # Loop ends here with url with value None if pagination were needed
                url = m.group(2) if m else None
            except:
                # Loop ends here if no pagination were needed
                break
        return result

    def get_record(
        self,
        sys_id: str,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a GET request to the instance table. Returns only one record, with the given sys_id.

        :param sys_id: Record unique ID.
        :param api_version: API version, if API versioning is enabled.
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        :rtype: dict
        """

        url = self.make_url(api_version, sys_id, **kwargs)
        if verbose:
            print(url)

        session = self.get_session(headers)
        response = session.get(url)
        self.check_status_code(response)

        return response.json()['result']

    def get_record_by_number(
        self,
        number: str,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a GET request to the instance table. Adds 'number' to the query parameters. 

        :param number: Record number.
        :param api_version: API version, if API versioning is enabled.
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: Other query parameters to the URL.
        :rtype: list
        """

        url = self.make_url(api_version, **kwargs)
        operator = '&' if kwargs else '?'
        url += f'{operator}number={number}'
        if verbose:
            print(url)

        session = self.get_session(headers)
        response = session.get(url)
        self.check_status_code(response)

        return response.json()['result']

    def patch(
        self,
        sys_id: str,
        data: dict,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a PATCH request to the instance table.

        :param sys_id: Record unique ID.
        :param data: Fields and values to update in the record.
        :param api_version: API version (if API versioning is enabled).
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        :rtype: dict
        """

        url = self.make_url(api_version, sys_id=sys_id, **kwargs)
        if verbose:
            print(url)
        session = self.get_session(headers)

        req_body = json.dumps(data)
        response = session.patch(url, req_body)
        self.check_status_code(response)

        result = response.json()
        return result['result']

    def post(
        self,
        data: dict,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a POST request to the instance table.

        :param data: Fields and values to the new record.
        :param api_version: API version (if API versioning is enabled).
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        :rtype: dict
        """

        url = self.make_url(api_version, **kwargs)
        if verbose:
            print(url)
        session = self.get_session(headers)

        req_body = json.dumps(data)
        response = session.post(url, req_body)
        self.check_status_code(response, 201)

        return response.json()['result']

    def put(
        self,
        sys_id: str,
        data: dict,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a PUT request to the instance table.

        :param sys_id: Record unique ID.
        :param data: New values to the record.
        :param api_version: API version (if API versioning is enabled).
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        :rtype: dict
        """

        url = self.make_url(api_version, sys_id=sys_id, **kwargs)
        if verbose:
            print(url)
        session = self.get_session(headers)

        req_body = json.dumps(data)
        response = session.put(url, req_body)
        self.check_status_code(response)

        result = response.json()
        return result['result']

    def delete(
        self,
        sys_id: str,
        api_version=None,
        headers={"Accept":"application/json","Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a DELETE request to the instance table.

        :param sys_id: Record unique ID.
        :param api_version: API version (if API versioning is enabled).
        :param headers: Request headers.
        :param verbose: If set to True, prints the full URL before it sends the request.
        :param **kwargs: All query parameters to the URL.
        """

        url = self.make_url(api_version, sys_id=sys_id, **kwargs)
        if verbose:
            print(url)
        session = self.get_session(headers)

        response = session.delete(url)
        self.check_status_code(response, 204)
        return response.content

    def get_session(self, headers):
        """
        Return a requests.Session object.

        :param headers: Request headers.
        """

        s = requests.Session()
        s.auth = self.__credentials
        s.headers.update(headers)
        return s

    def check_status_code(self, response: requests.models.Response, expected=200):
        """
        Checks if the given response status code is as expected.
        Raises a StatusCodeError if it is not.

        :param response: Response object.
        :param expected: Expected status code.
        """
        if response.status_code != expected:
            data = response.json()
            raise StatusCodeError(data["error"]["message"], data["error"]["detail"], response.status_code)

    def make_url(self, api_version=None, sys_id=None, **kwargs):
        """
        Returns a complete url to send in the request.

        :rtype: str
        """

        url = self.__instance_url
        if api_version:
            url += f'{api_version}/'
        url += f'table/{self.__table}'
        if sys_id:
            url += f'/{sys_id}'
        if kwargs:
            url += '?' + '&'.join([ f'{k}={v}' for k, v in kwargs.items() ])
        return url
