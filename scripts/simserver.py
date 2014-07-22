from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
 
class MyRequestHandler(BaseHTTPRequestHandler):
 
 
    def do_POST(self):
        self.do_GET() # currently same as post, but can be anything
 
def main():
    try:
        # you can specify any port you want by changing <q>81</q>
        server = HTTPServer((<q></q>, 81), MyRequestHandler)
        print <q>starting httpserver…</q>
        server.serve_forever()
    except KeyboardInterrupt:
        print <q>^C received, shutting down server</q>
        server.socket.close()
 
if __name__ == <q>__main__</q>:
    main()
