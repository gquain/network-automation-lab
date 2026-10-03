#!/usr/bin/env python3
"""
Mock Cisco IOS XE RESTCONF Server
Simulates /restconf/data/ietf-interfaces:interfaces with standard IETF YANG data model.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 8080

DATA = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {"name": "GigabitEthernet1", "description": "Uplink to Core", "enabled": True},
            {"name": "GigabitEthernet2", "description": "Data Subnet", "enabled": True},
            {"name": "GigabitEthernet3", "description": "Spare Interface", "enabled": False},
            {"name": "Loopback0", "description": "Router ID", "enabled": True}
        ]
    }
}

class RestconfHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/restconf/data/ietf-interfaces:interfaces":
            self.send_response(200)
            self.send_header("Content-Type", "application/yang-data+json")
            self.end_headers()
            self.wfile.write(json.dumps(DATA).encode("utf-8"))
        elif "interface=Loopback100" in self.path:
            loopback = next((i for i in DATA["ietf-interfaces:interfaces"]["interface"] if i["name"] == "Loopback100"), None)
            if loopback:
                self.send_response(200)
                self.send_header("Content-Type", "application/yang-data+json")
                self.end_headers()
                self.wfile.write(json.dumps({"ietf-interfaces:interface": loopback}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        new_intf = payload.get("ietf-interfaces:interface", {})

        interfaces = DATA["ietf-interfaces:interfaces"]["interface"]
        for idx, item in enumerate(interfaces):
            if item["name"] == new_intf.get("name"):
                interfaces[idx] = new_intf
                self.send_response(204)
                self.end_headers()
                return

        interfaces.append(new_intf)
        self.send_response(201)
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    print(f"[*] Cisco IOS XE RESTCONF Server running on http://{HOST}:{PORT}")
    print("[*] Ready to accept RESTCONF requests...")
    server = HTTPServer((HOST, PORT), RestconfHandler)
    server.serve_forever()