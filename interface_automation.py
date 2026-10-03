#!/usr/bin/env python3
"""
Task 3: interface_automation.py
Purpose: Programmatic Interface Provisioning and State Verification via RESTCONF
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://127.0.0.1:8080/restconf/data/ietf-interfaces:interfaces/interface=Loopback100"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

PAYLOAD = {
    "ietf-interfaces:interface": {
        "name": "Loopback100",
        "description": "Configured via RESTCONF Automation Lab Assignment",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.100.100.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
}

def configure_and_verify():
    print(f"Target RESTCONF Interface URL:\n  {BASE_URL}\n")

    # Step 1: Deploy Configuration using HTTP PUT
    print("[+] Step 1: Sending HTTP PUT configuration payload...")
    try:
        put_resp = requests.put(
            url=BASE_URL,
            headers=HEADERS,
            data=json.dumps(PAYLOAD),
            timeout=10
        )

        print(f"    HTTP Status Code: {put_resp.status_code}")
        if put_resp.status_code in [200, 201, 204]:
            print("    [SUCCESS] Interface Loopback100 successfully provisioned/updated on router.")
        else:
            print(f"    [FAILURE] Failed to provision interface. Response:\n    {put_resp.text}")
            return

        # Step 2: Retrieve and Verify Loopback100
        print("\n[+] Step 2: Retrieving Loopback100 configuration via HTTP GET...")
        get_resp = requests.get(
            url=BASE_URL,
            headers=HEADERS,
            timeout=10
        )

        print(f"    HTTP Status Code: {get_resp.status_code}")
        if get_resp.status_code == 200:
            data = get_resp.json().get("ietf-interfaces:interface", {})
            print("    [VERIFICATION SUCCESS] Operational parameters retrieved:")
            print(f"      - Interface Name : {data.get('name')}")
            print(f"      - Description    : {data.get('description')}")
            print(f"      - Admin State    : {'UP' if data.get('enabled') else 'DOWN'}")
            
            ipv4_cfg = data.get("ietf-ip:ipv4", {}).get("address", [{}])[0]
            print(f"      - IPv4 Address   : {ipv4_cfg.get('ip')}")
            print(f"      - Subnet Mask    : {ipv4_cfg.get('netmask')}")
        else:
            print(f"    [VERIFICATION FAILED] Server returned code: {get_resp.status_code}")

    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Communication error occurred: {err}")

if __name__ == "__main__":
    configure_and_verify()