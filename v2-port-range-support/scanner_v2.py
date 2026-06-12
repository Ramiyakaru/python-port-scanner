import socket
import sys
from tqdm import tqdm


def scan_port(host, port):
    """
    Returns True if port is open, otherwise False
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((host, port))
        return result == 0

    except Exception:
        return False

    finally:
        sock.close()


def parse_ports(port_args):
    """
    Converts user input into a list of ports.
    Supports:
    - Single ports (80)
    - Ranges (1-1000)
    """
    ports = []

    for arg in port_args:

        # Range support (e.g. 20-100)
        if "-" in arg:
            try:
                start, end = arg.split("-")
                start = int(start)
                end = int(end)

                for port in range(start, end + 1):
                    ports.append(port)

            except ValueError:
                print(f"[-] Invalid range ignored: {arg}")

        # Single port
        else:
            try:
                ports.append(int(arg))
            except ValueError:
                print(f"[-] Invalid port ignored: {arg}")

    return ports


if __name__ == "__main__":

    # Validate input
    if len(sys.argv) < 3:
        print("Usage: python scanner.py <Target IP> <Ports>")
        print("Examples:")
        print("  python scanner.py 192.168.1.10 80")
        print("  python scanner.py 192.168.1.10 22 80 443")
        print("  python scanner.py 192.168.1.10 1-1000")
        sys.exit(1)

    # Get target host
    target_host = sys.argv[1]

    # Get port arguments
    port_args = sys.argv[2:]

    # Convert input into actual port list
    ports_to_scan = parse_ports(port_args)

    print(f"\nStarting scan on: {target_host}")
    print(f"Total ports to scan: {len(ports_to_scan)}")
    print("-" * 50)

    # Scan each port with progress bar
for port in tqdm(
    ports_to_scan,
    desc="Scanning Ports",
    unit="port",
    ncols=100
):
    if scan_port(target_host, port):
        print(f"[+] Port {port} OPEN")
    else:
        print(f"[-] Port {port} CLOSED or FILTERED")

    print("-" * 50)
    print("Scan complete")