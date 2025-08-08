# Multi_Threaded_Port_Scanner
This is a multi threaded port scanner wrote in Python.

Example usage:
python3 multi_thread_port_scanner.py scanme.nmap.org -p 1-1056 -t 50 -o open_ports.txt

Information on the website we're scanning ports from: http://scanme.nmap.org/

usage: multi_thread_port_scanner.py [-h] [-p PORTS] [-t THREADS] [-o OUTPUT] target

Fast Python Port Scanner

positional arguments:
  target                Target host or IP address

options:
  -h, --help            show this help message and exit
  -p, --ports PORTS     Port range, e.g. 1-1024
  -t, --threads THREADS
                        Number of threads
  -o, --output OUTPUT   File to save open ports
