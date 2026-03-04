import http.server
import socketserver

PORT = 5500

class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Optionnel : afficher les fichiers servis
    def log_message(self, format, *args):
        print(self.address_string(), "-", format % args)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving HTML on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
