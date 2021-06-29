from http.server import BaseHTTPRequestHandler, HTTPServer
from MetalnessCalculator import MetalnessCalculator
import time

hostName = "localhost"
serverPort = 8080

class Server(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        print("constructing server..")
        self.metalCalculator = MetalnessCalculator()
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>How Metal is this?</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>POST strings to this address to find out how metal they are!</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode('utf-8')
        print(post_body)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        response = str(self.metalCalculator.calculate_words_metalness(post_body)).encode()
        self.wfile.write(response)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Server)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
