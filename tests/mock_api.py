from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from threading import Thread


CORRECT_CHALLENGE = "HTB{a_challenge_flag}"
CORRECT_HASH = "30ea86803e0d85be51599c3a4e422266"


class MockApiHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        if self.path == "/api/v4/challenge/own":
            if message['flag'] == CORRECT_CHALLENGE:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Congratulations"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Incorrect flag"}).encode())
        elif self.path == "/api/v4/machine/own":
            if message['flag'] == CORRECT_HASH:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Congratulations"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Incorrect flag!"}).encode())
        elif self.path == "/api/v4/login":
            self._set_headers()
            self.wfile.write(json.dumps({
                "message": {
                    "access_token": "FakeToken",
                    "refresh_token": "FakeToken"
                }
            }).encode())


def start_mock_server():
    mock_server = HTTPServer(('localhost', 9000), MockApiHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
