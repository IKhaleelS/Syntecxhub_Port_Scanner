import socket
import threading
import argparse
import logging
from datetime import datetime
from services import SERVICES

# Colors
GREEN = "\033[92m"
RESET = "\033[0m"

# Store open ports
open_ports = []

# Logging
logging.basicConfig(
    filename="scan_results.txt",
    level=logging.INFO,
    format="%(message)s",
    filemode="a"
)

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        if sock.connect_ex((host, port)) == 0:
            service = SERVICES.get(port, "Unknown")

            result = f"[OPEN] {host}: PORT {port} | Service: {service}"
            print(GREEN + result + RESET)
            logging.info(result)

            open_ports.append(port)

        sock.close()
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Port Scanner v3.1 (Clean)")
    parser.add_argument("--host", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)

    args = parser.parse_args()

    print(f"\nScanning Host: {args.host}")
    print(f"Port Range: {args.start} - {args.end}\n")
    logging.info("Scanner Initialized Successfully")

    logging.info("\n==============================")
    logging.info(f"Scan started: {datetime.now()}")
    logging.info(f"Host: {args.host}")
    logging.info(f"Ports: {args.start} - {args.end}")

    threads = []

    for port in range(args.start, args.end + 1):
        t = threading.Thread(target=scan_port, args=(args.host, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    summary = f"\nScan Complete: {len(open_ports)} open ports found."
    print(summary)
    logging.info(summary)
    logging.info("==============================\n")

if __name__ == "__main__":
    main()
