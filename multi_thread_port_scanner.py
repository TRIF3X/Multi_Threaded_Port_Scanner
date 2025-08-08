import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
import threading




# Thread-safe counter for progress
progress_lock = threading.Lock()
ports_scanned = 0

# List to store open ports
open_ports = []

# Function to scan a single port on the target
def scan_port(target, port):
    try:
        # Create a new socket object using IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout so the socket doesn’t wait forever
        socket.setdefaulttimeout(0.5)
        # Attempt to connect to the target IP and port
        result = sock.connect_ex((target, port))
        # connect_ex returns 0 if connection succeeded (port is open)
        if result == 0:
            with progress_lock:
                open_ports.append(port)
            return port # Return open port
        # Close the socket after checking
        sock.close()
    except Exception:
        # Ignore exceptions (e.g., network errors)
        pass
    finally:
        # Update progress counter safely
        with progress_lock:
            global ports_scanned
            ports_scanned += 1
            print(f"\rScanned {ports_scanned} ports", end='')
    return None

if __name__ == "__main__":
    # Create an argument parser to handle command-line inputs
    parser = argparse.ArgumentParser(description="Fast Python Port Scanner")
    # Required positional argument: target host or IP
    parser.add_argument("target", help="Target host or IP address")
    # Optional argument for port range, default is 1-1024
    parser.add_argument("-p", "--ports", help="Port range, e.g. 1-1024", default="1-1024")
    # Optional argument for number of threads to use, default is 50
    parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=50)
    # Optional argument for outputting open ports to file
    parser.add_argument("-o", "--output", help="File to save open ports", default=None)
    # Parse the command-line arguments
    args = parser.parse_args()

    # Parse the port range string "start-end" into two integers
    start_port, end_port = map(int, args.ports.split("-"))
    total_ports = end_port - start_port + 1

    print(f"Starting scan on {args.target} ports {start_port} to {end_port} with {args.threads} threads.")


    # Create a ThreadPoolExecutor to manage a pool of worker threads
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Submit a scan_port task for each port in the specified range
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, args.target, port)

    print("\nScan complete!")
    if open_ports:
        print("Open ports:")
        for port in sorted(open_ports):
            print(f" - {port}")
    else:
        print("No open ports found.")

    # Save results if output file specified
    if args.output:
        try:
            with open(args.output, "w") as f:
                for port in sorted(open_ports):
                    f.write(f"{port}\n")
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error saving results: {e}")




# socket: For network communication and testing ports.
# argparse: To get user input from the command line in a flexible way.
# ThreadPoolExecutor from concurrent.futures: To run many port scans concurrently with threads.

# Function scan_port(target, port)
# Creates a TCP socket (socket.AF_INET, socket.SOCK_STREAM).
# Sets a short timeout (0.5 seconds) so the scan doesn’t hang.
# Attempts to connect to the given target and port using connect_ex().
# Returns 0 if connection succeeded → port is open.
# If open, prints a message.
# Closes the socket afterward.
# Uses try-except to ignore errors like unreachable hosts or blocked ports.

# Main program (if __name__ == "__main__":)
# Sets up command-line arguments for target host/IP, port range, and number of threads.
# Parses the port range string like "1-1024" into two integers for the loop.
# Creates a thread pool with specified max workers (args.threads).
# Submits a scanning job for each port in the range, which the threads execute concurrently.
# This lets you scan many ports in parallel, making the scan much faster than scanning sequentially.
