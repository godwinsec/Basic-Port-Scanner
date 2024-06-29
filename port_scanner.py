import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """
    Function to scan a single port on a given IP address.
    Returns True if the port is open, else returns False.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout of 1 second
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False

def scan_ports(ip, start_port, end_port, num_threads):
    """
    Function to scan a range of ports on a given IP address.
    Uses multithreading to speed up the scanning process.
    """
    open_ports = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in future_to_port:
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
    return open_ports

def main():
    """
    Main function to run the port scanner.
    """
    ip = input("Enter IP address to scan: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    num_threads = int(input("Enter number of threads: "))

    print(f"Scanning {ip} from port {start_port} to {end_port} with {num_threads} threads...")
    open_ports = scan_ports(ip, start_port, end_port, num_threads)

    if open_ports:
        print(f"Open ports on {ip}: {open_ports}")
    else:
        print(f"No open ports found on {ip}.")

if __name__ == "__main__":
    main()
