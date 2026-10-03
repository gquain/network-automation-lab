#!/usr/bin/env python3
"""
Task 2: restconf_monitor.py
Purpose: RESTCONF Network Monitoring Script
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "http://127.0.0.1:8080/restconf/data/ietf-interfaces:interfaces"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

def monitor_interfaces():
    print(f"Connecting to RESTCONF endpoint: {URL}...")
    try:
        response = requests.get(
            url=URL,
            headers=HEADERS,
            timeout=10
        )

        print(f"HTTP Response Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            interfaces = data.get("ietf-interfaces:interfaces", {}).get("interface", [])

            print("\n" + "=" * 60)
            print(f"{'INTERFACE NAME':<35} | {'ENABLED / ADMIN STATUS':<20}")
            print("=" * 60)

            for intf in interfaces:
                name = intf.get("name", "Unknown")
                enabled = intf.get("enabled", False)
                status_str = "ENABLED (UP)" if enabled else "DISABLED (DOWN)"
                print(f"{name:<35} | {status_str:<20}")
            print("=" * 60)
        else:
            print(f"[!] Server returned status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Failed to establish connection. Is mock_cisco_router.py running?")
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] An unexpected error occurred: {err}")

if __name__ == "__main__":
    monitor_interfaces()