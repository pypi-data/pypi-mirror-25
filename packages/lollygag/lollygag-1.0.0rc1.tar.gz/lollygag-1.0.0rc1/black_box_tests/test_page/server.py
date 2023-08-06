#!/usr/bin/env python

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except (ImportError, ModuleNotFoundError):
    from http.server import SimpleHTTPRequestHandler

PORT = 80

def main():
    print ("Starting a new test server")
    httpd = SocketServer.TCPServer(("localhost", PORT), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
