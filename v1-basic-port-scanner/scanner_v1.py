import socket
import sys


def scan_port(host, port):
    """
    Returns True if port is open, otherwise False
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((host, port))

        if result == 0:
            return True
        else:
            return False

    except Exception:
        return False

    finally:
        sock.close()


if __name__ == "__main__":

    # Ensure at least host + one port is provided
    if len(sys.argv) < 3:
        print("Usage: python scanner.py <Target IP> <Port1> <Port2> ...")
        print("Example: python scanner.py 192.168.1.10 22 80 443")
        sys.exit(1)

    # Extract target host
    target_host = sys.argv[1]

    # Extract ports and convert to integers safely
    ports_to_scan = []

    for arg in sys.argv[2:]:
        try:
            ports_to_scan.append(int(arg))
        except ValueError:
            print(f"[-] Ignoring invalid port: {arg}")

    print(f"\nStarting scan on host: {target_host}")
    print("-" * 40)

    # Scan each port
    for target_port in ports_to_scan:
        is_open = scan_port(target_host, target_port)

        if is_open:
            print(f"[+] Port {target_port} OPEN")
        else:
            print(f"[-] Port {target_port}: CLOSED or FILTERED")

    print("-" * 40)
    print("Scan complete")