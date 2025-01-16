# EvilJam - The Ultimate WiFi Jammer

EvilJam is a powerful tool designed for educational purposes to demonstrate WiFi jamming and handshake capturing techniques. This tool allows you to scan for WiFi networks, capture handshakes, and perform deauthentication attacks on clients connected to a target WiFi network.

## Features

- Scan for available WiFi networks
- Capture WPA/WPA2 handshakes
- Perform deauthentication attacks on all clients or specific clients
- Activate and deactivate monitor mode on network interfaces
- Crack captured handshakes using a wordlist

## Screensshots

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
3. The tool will use `aircrack-ng` to attempt to crack the password using the selected wordlist.

## Special Features

### Jam Specific Client

EvilJam allows you to perform deauthentication attacks on specific clients connected to a target WiFi network. This feature can be accessed through the "WiFi Jam" option, where you can choose to jam all clients or a specific client.

## Disclaimer

This tool is provided for educational purposes only. Unauthorized use of this tool may violate laws in your jurisdiction. The authors and contributors are not responsible for any misuse or damage caused by this tool.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Credits

- Tool owned by: DaddyDark
- Special thanks to all contributors.
