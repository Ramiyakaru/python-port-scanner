import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((host, port))
        return port, result == 0

    except Exception:
        return port, False

    finally:
        sock.close()


def grab_banner(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        sock.connect((host, port))

        banner = sock.recv(1024).decode(errors="ignore").strip()

        sock.close()

        return banner if banner else "Unknown Service"

    except Exception:
        return "Unknown Service"


def parse_ports(port_args):
    ports = []

    for arg in port_args:

        if "-" in arg:
            try:
                start, end = map(int, arg.split("-"))
                ports.extend(range(start, end + 1))
            except ValueError:
                print(f"Invalid range: {arg}")

        else:
            try:
                ports.append(int(arg))
            except ValueError:
                print(f"Invalid port: {arg}")

    return ports


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python scanner.py <IP> <ports>")
        sys.exit(1)

    target_host = sys.argv[1]
    ports_to_scan = parse_ports(sys.argv[2:])

    print(f"\nScanning {target_host}")
    print("-" * 50)

    def worker(port):
        port, is_open = scan_port(target_host, port)

        if is_open:
            banner = grab_banner(target_host, port)
            return f"[+] Port {port} OPEN | {banner}"

        return f"[-] Port {port} CLOSED or FILTERED"

    with ThreadPoolExecutor(max_workers=100) as executor:

        results = list(
            tqdm(
                executor.map(worker, ports_to_scan),
                total=len(ports_to_scan),
                desc="Scanning Ports",
                unit="port",
                ncols=100
            )
        )

    print()

    for result in results:
        print(result)
        
print("-" * 50)
print("Scan complete")