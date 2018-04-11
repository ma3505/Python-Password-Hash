import cgi
import hashlib
import uuid  # Universally Unique Identifiers for Salt
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

PORT_NUMBER = 8080


class PasswordHttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path == "/":
                self.path = "/index.html"
                f = open(curdir + sep + self.path)
                # Send 200 Response
                self.send_response(200)
                # Send Headers
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                # Send file contents to client
                self.wfile.write(f.read())
                f.close
                return
        except IOError:
            self.send_error(404, 'file_not_found')

    # Handler for the POST Request for password hash
    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        # START HASH PROCESS
        usr_input = form.getvalue("password")  # string Password
        # CREATE SALT
        salt = uuid.uuid4().hex
        # Add salt to Password
        usr_input = usr_input + salt
        # Convert to bytes
        usr_bytes = bytes(usr_input)

        # Hash the Bytes
        hash_obj = hashlib.sha256(usr_bytes)
        # Convert to Hex Value for Output
        hex_pass = hash_obj.hexdigest()

        # Request Information
        # print("\n--------Request Start--------->\n")
        # request_headers = self.headers
        # content_length = request_headers.getheaders('content-length')
        # data = int(content_length[0])
        # print(request_headers)
        # print(self.rfile.read(data))
        # print("<--------Request End ------------>\n")

        print("\n--------------SALT--------->\n")
        print(salt)
        print("\n---------------Hashed Password---------------->\n")
        # HASH INFORMATION
        print(hex_pass)
        self.send_response(200)


def run():
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', PORT_NUMBER), PasswordHttpRequestHandler)
        print 'Started httpserver on port:', PORT_NUMBER

        # Wait forever for incoming htto requests
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C Received Shutting Down Server'
        server.socket.close()


if __name__ == '__main__':
    run()
