import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from views import (create_entry, delete_entry, get_all_entries,
                   get_entries_by_search, get_single_entry, get_single_mood,
                   update_entry)
from views.mood_requests import get_all_moods


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, POST, PUT, DELETE requests to the server"""

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow_Origin headers
        on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('COntent-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def parse_url(self):
        """returns parts of our url as a tuple

        Returns:
            tuple: the resource and the id
        """
        path_params = self.path.split("/")
        resource = path_params[1]

        if "?" in resource:
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

    def do_OPTIONS(self):
        """Sets the options headers
        """

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_POST(self):
        """Performs a POST request to the server
        """

        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        resource, _ = self.parse_url()  # pylint: disable=unbalanced-tuple-unpacking

        new_entry = None

        if resource == "entries":
            new_entry = create_entry(post_body)
            self.wfile.write(f"{new_entry}".encode())

    def do_PUT(self):
        """Performs a PUT request to the server
        """

        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        resource, id = self.parse_url()  # pylint: disable=unbalanced-tuple-unpacking

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_GET(self):
        """Performs a GET request to the server
        """

        self._set_headers(200)

        response = {}

        parsed = self.parse_url()

        if len(parsed) == 2:
            resource, id = parsed   # pylint: disable=unbalanced-tuple-unpacking

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"

        elif len(parsed) == 3:
            resource, key, value = parsed

            if resource == "entries" and key == "q":
                response = f"{get_entries_by_search(value)}"

        self.wfile.write(response.encode())

    def do_DELETE(self):
        """Performs a DELETE request to the server
        """
        self._set_headers(204)

        resource, id = self.parse_url()  # pylint: disable=unbalanced-tuple-unpacking

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
