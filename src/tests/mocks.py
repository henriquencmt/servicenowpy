import json
import re
import socket
import requests

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class MockServerRequestHandler(BaseHTTPRequestHandler):
    INC_PATTERN = re.compile(r'/incident')
    INC_SYS_ID_PATTERN = re.compile(r'/incident/([^\?]+)')

    def do_GET(self):
        if re.search(self.INC_PATTERN, self.path):
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json;charset=UTF-8')
            self.end_headers()

            m = re.search(self.INC_SYS_ID_PATTERN, self.path)
            if m:
                response_content = json.dumps({
                    "result": read_mock_data(single_record=True)
                })
            else:
                response_content = json.dumps({
                    "result": read_mock_data()
                })
            self.wfile.write(response_content.encode('utf-8'))
            return
        else:
            self.send_response(requests.codes.not_found)

            self.send_header('Content-Type', 'application/json;charset=UTF-8')
            self.end_headers()

            response_content = json.dumps({
                "error": {
                    "message": "Mock Not Found",
                    "detail": "Mock is working as expected"
                }
            })
            self.wfile.write(response_content.encode('utf-8'))
            return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


def read_mock_data(single_record=False):
    with open('tests/mock_data.json') as f:
        data = json.load(f)
        return data if not single_record else data[0]