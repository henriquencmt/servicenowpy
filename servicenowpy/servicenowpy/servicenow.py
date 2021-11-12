import json
import re
import requests

from .exceptions import StatusCodeError

class Client:
    """
    Represents a ServiceNow's instance.
    """

    def __init__(self, instance_url, user, pwd):
        self.__instance_url = self.make_api_url(instance_url)
        self.__credentials = user, pwd

    def make_api_url(self, instance_url):
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
    """

    def __init__(self, table, instance_url, credentials: tuple):
        """
        :param table: The table name.
        :param instance_url: ServiceNow instance URL, with or without "https://".
        :param credentials: Tuple containing user and password, respectively.
        """

        self.__table = table
        self.__instance_url = instance_url
        self.__credentials = credentials

    def get(self, api_version=None, headers={"Accept":"application/json"}, verbose=False, **kwargs):
        """
        Sends a GET request to the instance table.

        :param api_version: API version (if API versioning is enabled).
        :param **kwargs: All query parameters to the URL.
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
        data: str,
        api_version=None,
        headers={"Accept":"application/json"},
        verbose=False,
        **kwargs
    ):
        """
        Sends a PATCH request to the instance table.

        :param api_version: API version (if API versioning is enabled).
        :param **kwargs: All query parameters to the URL.
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

        :param api_version: API version (if API versioning is enabled).
        :param **kwargs: All query parameters to the URL.
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

        :param api_version: API version (if API versioning is enabled).
        :param **kwargs: All query parameters to the URL.
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

        :param api_version: API version (if API versioning is enabled).
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
        """

        s = requests.Session()
        s.auth = self.__credentials
        s.headers.update(headers)
        return s

    def check_status_code(self, response, expected=200):
        if response.status_code != expected:
            data = response.json()
            raise StatusCodeError(data["error"]["message"], data["error"]["detail"], response.status_code)

    def make_url(self, api_version=None, sys_id=None, **kwargs):
        url = self.__instance_url
        if api_version:
            url += f'{api_version}/'
        url += f'table/{self.__table}'
        if sys_id:
            url += f'/{sys_id}'
        if kwargs:
            url += '?' + '&'.join([ f'{k}={v}' for k, v in kwargs.items() ])
        return url
