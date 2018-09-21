#!/usr/bin/env python3.7

import click
import socket
import sys
import re
import threading
from command_patterns import CommandPatterns
from status import Status


@click.command()
@click.option('--port', default=5245, help='Port the daemon listens on.')
@click.option('--host', default='', help='Host the daemon listens on.')
def create_socket():
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return tcp_socket
    except socket.error as msg:
        print(
            "Could not create socket. Error Code: ",
            str(msg[0]),
            "Error: ",
            msg[1]
        )
        sys.exit(0)


def bind_socket(tcp_socket, host, port):
    try:
        tcp_socket.bind((host, port))
        print("[-] Socket Bound to port " + str(port))
    except socket.error as msg:
        print(
            "Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1])
        )
        sys.exit()


def receive_command(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
    return data


def get_revision(connection, revision_number):
    pass


def handle_command(connection, command):
    get_pattern = re.compile(CommandPatterns.get)
    get_match = get_pattern.match(command)
    if get_match is not None:
        revision_number = get_match.group('revision')
        get_revision(connection, revision_number)
    connection.sendall(Status.command_not_found)


def client_thread(connection):
    command = receive_command(connection)
    handle_command(connection, command)

    connection.close()


def start_connection_handler(host, port):
    """Daemon that calculates the diff for SFTP and submits it via TCP"""
    tcp_socket = create_socket()
    bind_socket(tcp_socket, host, port)
    tcp_socket.listen()

    while True:
        connection, address = tcp_socket.accept()
        print("[-] Connected to " + address[0] + ":" + str(address[1]))
        threading.Thread(
            target=client_thread,
            kwargs={'connection': connection}
        ).start()


if __name__ == '__main__':
    start_connection_handler()
