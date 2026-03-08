import subprocess
import sys
import time

def run_command(command):
    """Executes a shell command and returns the output."""
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    return result.returncode == 0

def create_hotspot(ssid, password, ifname="wlan0"):
    """
    Creates and activates a Wi-Fi hotspot using NetworkManager 
    via nmcli.
    """
    print(f"Setting up Wi-Fi 6 Hotspot: {ssid} on {ifname}...")
    
    # Step 1: Check if the connection already exists and remove it to restart fresh
    subprocess.run(["nmcli", "connection", "delete", ssid], capture_output=True)

    # Step 2: Create a new Wi-Fi Access Point (Hotspot) connection
    # We specify the 802-11-wireless interface type and ap mode.
    create_cmd = [
        "nmcli", "device", "wifi", "hotspot",
        "ifname", ifname,
        "ssid", ssid,
        "password", password
    ]
    
    if run_command(create_cmd):
        print(f"Hotspot {ssid} successfully activated. Waiting for IoT devices to join...")
    else:
        print(f"Failed to activate hotspot {ssid}.")

def stop_hotspot(ssid):
    """
    Stops and removes the Wi-Fi hotspot profile.
    """
    print(f"Stopping hotspot {ssid}...")
    
    # By deleting the connection profile, NetworkManager tears it down automatically.
    stop_cmd = [
        "nmcli", "connection", "delete", "Hotspot" # often defaults to Hotspot unless explicitly named
    ]
    # As a fallback, try deleting by SSID name as well
    subprocess.run(stop_cmd, capture_output=True)
    subprocess.run(["nmcli", "connection", "delete", ssid], capture_output=True)
    print("Hotspot stopped.")

def connect_to_wifi(ssid, password):
    """
    Connects to an existing infrastructure Wi-Fi Network.
    """
    print(f"Connecting to Network: {ssid}...")
    connect_cmd = [
        "nmcli", "device", "wifi", "connect", ssid, "password", password
    ]
    
    if run_command(connect_cmd):
         print(f"Successfully connected to {ssid}.")
    else:
         print(f"Failed to connect to {ssid}.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 wifi_manager.py [start-hotspot|stop-hotspot|connect] <ssid> [password]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "start-hotspot":
        if len(sys.argv) < 4:
            print("Usage for hotspot: python3 wifi_manager.py start-hotspot <ssid> <password>")
            sys.exit(1)
        create_hotspot(sys.argv[2], sys.argv[3])
        
    elif action == "stop-hotspot":
        if len(sys.argv) < 3:
            print("Usage for stop: python3 wifi_manager.py stop-hotspot <ssid>")
            sys.exit(1)
        stop_hotspot(sys.argv[2])
        
    elif action == "connect":
        if len(sys.argv) < 4:
            print("Usage for connect: python3 wifi_manager.py connect <ssid> <password>")
            sys.exit(1)
        connect_to_wifi(sys.argv[2], sys.argv[3])
    else:
        print("Invalid action.")
