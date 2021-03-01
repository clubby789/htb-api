from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
from threading import Thread


CORRECT_CHALLENGE = "HTB{a_challenge_flag}"
CORRECT_HASH = "30ea86803e0d85be51599c3a4e422266"

has_ratelimited: bool = False


class MockApiHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        global has_ratelimited
        if not has_ratelimited:
            # Simulate ratelimit by sending a 429 once
            self.send_response(429)
            self.end_headers()
            has_ratelimited = True
            self.wfile.write(b"")
            return
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
        elif self.path == "/api/v4/challenge/start":
            if message['challenge_id'] == 144:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Instance Created!", "id": "pwnhunting-83743",
                                             "port": 31475, "ip": "10.10.10.10"}).encode()
                                 )
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Incorrect Parameters"}).encode())

        elif self.path == "/api/v4/challenge/stop":
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Container Stopped"}).encode())

        elif re.match(r"/api/v4/endgame/\d+/flag", self.path):
            if message['flag'] == CORRECT_HASH:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Congratulations"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Wrong flag"}).encode())
        elif re.match(r"/api/v4/fortress/\d+/flag", self.path):
            if message['flag'] == CORRECT_HASH:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Congratulations"}).encode())
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Wrong flag"}).encode())

    def log_message(self, fmt, *args):
        # Silence logging
        return


def start_mock_server():
    mock_server = HTTPServer(('localhost', 9000), MockApiHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()
