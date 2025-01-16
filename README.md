# EvilJam - The Ultimate WiFi Jammer

EvilJam is a powerful tool designed for educational purposes to demonstrate WiFi jamming and handshake capturing techniques. This tool allows you to scan for WiFi networks, capture handshakes, and perform deauthentication attacks on clients connected to a target WiFi network.

## Features

- Scan for available WiFi networks
- Capture WPA/WPA2 handshakes
- Perform deauthentication attacks on all clients or specific clients
- Activate and deactivate monitor mode on network interfaces
- Crack captured handshakes using a wordlist

## Screensshots

![Image](https://github.com/user-attachments/assets/1817338d-ab8a-4e2a-a286-55f9eddde212)

![Image](https://github.com/user-attachments/assets/63bbefc6-2577-4fd5-9f2d-687dcb18fcbd)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/EvilJam.git
    cd EvilJam
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Install the external tools using your package manager. For Debian-based systems (e.g., Ubuntu, Kali Linux), use:

    ```sh
    sudo apt-get update
    sudo apt-get install aircrack-ng iw net-tools
    ```

## Usage

1. Run the [EvilJam.py](http://_vscodecontentref_/0) script with root privileges:

    ```sh
    sudo python3 EvilJam.py
    ```

2. Follow the on-screen instructions to choose an option from the main menu.

## Main Menu Options

1. **WiFi Jam**: Scan for WiFi networks and perform deauthentication attacks.
2. **Capture Handshake**: Capture WPA/WPA2 handshakes from a target WiFi network.
3. **Activate Monitor Mode**: Activate monitor mode on a network interface.
4. **Activate Managed Mode**: Deactivate monitor mode and switch to managed mode on a network interface.
5. **Crack Handshake**: Crack the password of a captured handshake using a wordlist.
6. **Credits**: Display credits and tool information.
7. **Exit**: Exit the tool.



## Cracking Passwords

To crack the password of a captured handshake, follow these steps:

1. Capture the handshake using the "Capture Handshake" option.
2. Use the "Crack Handshake" option to select the captured handshake file and a wordlist.

## Special Features

### Jam All Clients

EvilJam allows you to perform deauthentication attacks on all clients connected to a target WiFi network. This feature can be accessed through the "WiFi Jam" option, where you can choose to jam all clients. This is useful for testing the security and resilience of a network by simulating a denial-of-service attack.

### Jam Specific Client

EvilJam allows you to perform deauthentication attacks on specific clients connected to a target WiFi network. This feature can be accessed through the "WiFi Jam" option, where you can choose to jam a specific client. This is particularly useful for targeting specific devices without disrupting the entire network.

### Capture Handshake

EvilJam provides an easy way to capture WPA/WPA2 handshakes from a target WiFi network. This feature can be accessed through the "Capture Handshake" option. The captured handshakes can be used for offline password cracking.

### Easily Crack Handshake

EvilJam allows you to easily crack the password of a captured handshake using a wordlist. This feature can be accessed through the "Crack Handshake" option. The tool uses `aircrack-ng` to attempt to crack the password, and the results are saved to a file for later reference.

### Easy to Use Interface

EvilJam provides a user-friendly interface with clear instructions and options. The main menu allows you to easily navigate through different features and functionalities. The tool also provides detailed feedback and status updates during operations, making it easy to understand what is happening at each step.

### Comprehensive Network Scanning

EvilJam includes robust network scanning capabilities, allowing you to detect and list all available WiFi networks and clients. The tool provides detailed information about each network, including the ESSID, BSSID, and channel, helping you make informed decisions about which network to target.

### Flexible Attack Options

EvilJam offers flexible attack options, allowing you to perform deauthentication attacks on all clients or specific clients. You can also capture WPA/WPA2 handshakes for later analysis and password cracking. The tool supports both automated and manual attack modes, giving you full control over the attack process.

### Monitor and Managed Mode Switching

EvilJam makes it easy to switch between monitor mode and managed mode on your network interfaces. This is essential for performing network scans and attacks, as well as returning your interface to normal operation after the attack.

## Disclaimer

This tool is provided for educational purposes only. Unauthorized use of this tool may violate laws in your jurisdiction. The authors and contributors are not responsible for any misuse or damage caused by this tool.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

- Tool owned by: DaddyDark
- Special thanks to all contributors.
