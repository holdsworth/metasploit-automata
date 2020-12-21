import socket
import random

ERROR_CODES = [0, 61, 110]


def is_port_closed(lhost: str, port_number: int):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = (lhost, port_number)
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()
    if result_of_check in ERROR_CODES:
        return False

    return True


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # google dns server
    return s.getsockname()[0]


def generate_port():
    return random.randint(4443, 5000)


def generate_open_port(lhost):
    port = generate_port()
    while is_port_closed(lhost, port):
        port = generate_port()

    return port
