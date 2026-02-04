import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

FILE_DATA = "data_kas.json"
PORT = 8000


def load_data():
    if not os.path.exists(FILE_DATA):
        with open(FILE_DATA, "w") as f:
            json.dump({"kas": []}, f, indent=4)
    with open(FILE_DATA, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_DATA, "w") as f:
        json.dump(data, f, indent=4)


class KasHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/data":
            data = load_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        if self.path == "/tambah":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            transaksi = json.loads(body)

            data = load_data()
            data["kas"].append(transaksi)
            save_data(data)

            self.send_response(200)
            self.end_headers()


print("======================================")
print(" SERVER KAS TAKMIR BERJALAN ")
print(f" PORT : {PORT}")
print("======================================")

HTTPServer(("0.0.0.0", PORT), KasHandler).serve_forever()
