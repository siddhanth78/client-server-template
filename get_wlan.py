import netifaces

def get_wifi_ip():
    """Retrieves the Wi-Fi IP address."""
    gateways = netifaces.gateways()
    wifi_interface = gateways['default'][netifaces.AF_INET][1]
    ip_address = netifaces.ifaddresses(wifi_interface)[netifaces.AF_INET][0]['addr']
    return ip_address

if __name__ == "__main__":
    wifi_ip = get_wifi_ip()
    print(f"Wi-Fi IP address: {wifi_ip}")
