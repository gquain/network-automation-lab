#!/usr/bin/env python3
"""
Task 1: network_inventory.py
Purpose: Network Inventory Management Tool using Python Lists & Dictionaries
"""

def main():
    # 1. Store devices using a list of dictionaries
    inventory = [
        {
            "hostname": "R1-CORE-EDGE",
            "ip_address": "192.168.10.1",
            "device_type": "Cisco ISR4331",
            "location": "Data Center A - Rack 01",
            "status": "up"
        },
        {
            "hostname": "SW1-DIST-ACC",
            "ip_address": "192.168.20.10",
            "device_type": "Cisco Catalyst 9300",
            "location": "Building 2 - IDF Floor 1",
            "status": "up"
        },
        {
            "hostname": "R2-BRANCH-OFFICE",
            "ip_address": "10.0.50.1",
            "device_type": "Cisco Catalyst 8000V",
            "location": "Branch Office Cebu",
            "status": "down"
        },
        {
            "hostname": "SW2-CAMPUS-CORE",
            "ip_address": "192.168.1.254",
            "device_type": "Cisco Catalyst 9500",
            "location": "Data Center B - Rack 04",
            "status": "up"
        }
    ]

    print("=" * 80)
    print(f"{'NETWORK INVENTORY MANAGEMENT SYSTEM':^80}")
    print("=" * 80)

    # 2. Display all devices
    print("\n[+] COMPLETE DEVICE INVENTORY:")
    header = f"{'Hostname':<18} {'IP Address':<16} {'Device Type':<22} {'Location':<18} {'Status':<6}"
    print(header)
    print("-" * 80)
    for dev in inventory:
        print(f"{dev['hostname']:<18} {dev['ip_address']:<16} {dev['device_type']:<22} {dev['location']:<18} {dev['status'].upper():<6}")

    # 3. Display only devices with status UP and calculate operational total
    print("\n[+] OPERATIONAL DEVICES (STATUS: UP):")
    print(header)
    print("-" * 80)
    operational_count = 0
    for dev in inventory:
        if dev["status"].lower() == "up":
            operational_count += 1
            print(f"{dev['hostname']:<18} {dev['ip_address']:<16} {dev['device_type']:<22} {dev['location']:<18} {dev['status'].upper():<6}")

    # 4. Count and summary
    print("-" * 80)
    print(f"Total Managed Devices      : {len(inventory)}")
    print(f"Operational Devices (UP)   : {operational_count}")
    print(f"Non-Operational (DOWN)     : {len(inventory) - operational_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()