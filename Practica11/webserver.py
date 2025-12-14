import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

from networking import ClientUDP


class MiniApp:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=("GET",)):
        def decorator(handler):
            for method in methods:
                self.routes[(path, method.upper())] = handler
            return handler
        return decorator

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET").upper()
        handler = self.routes.get((path, method))
        if handler is None:
            start_response("404 Not Found", [
                           ("Content-Type", "text/plain; charset=utf-8")])
            return [b"Not Found"]
        response = handler(environ)
        status, headers, body = self._normalize_response(response)
        start_response(status, headers)
        return [body]

    def _normalize_response(self, response):
        if isinstance(response, tuple):
            status, headers, body = response
            body_bytes = body if isinstance(
                body, bytes) else body.encode("utf-8")
            return status, headers, body_bytes
        body_bytes = response if isinstance(
            response, bytes) else response.encode("utf-8")
        return "200 OK", [("Content-Type", "text/html; charset=utf-8")], body_bytes


app = MiniApp()
pwd_client = ClientUDP()


@app.route("/")
def serve_index(environ):
    with open("templates/index.html", "r", encoding="utf-8") as fp:
        html = fp.read().replace("{{name}}", "Carlos")
    return html


@app.route("/login")
def handle_login(environ):
    query_string = environ.get("QUERY_STRING", "")
    params = parse_qs(query_string)
    name = params.get("name", ["User"])[0]
    pwd = params.get("pwd", ["User"])[0]
    pwd_client.send_to(f"{name}:{pwd}", "192.168.1.50", 8080)
    message = pwd_client.listen()
    _, code = message.get("data", {}).split(":")

    if code == "OK":
        with open("templates/success.html", "r", encoding="utf-8") as fp:
            return fp.read().replace("{{name}}", name)
    else:
        with open("templates/error.html", "r", encoding="utf-8") as fp:
            return fp.read().replace("{{name}}", name)


@app.route("/health")
def health_check(environ):
    return "OK"


def run_server():
    server_ip = os.environ.get("WEBSERVER_HOST", "0.0.0.0")
    server_port = int(os.environ.get("WEBSERVER_PORT", "8000"))
    server = make_server(server_ip, server_port, app)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
