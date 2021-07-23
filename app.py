#!/usr/bin/env python
import socketserver
import signal
import argparse
import sys
from httphandler import HttpHandler


def sigint_handler(sig, frame):
    try:
        server.server_close()
        print('\nServer closed\n')
    finally:
        sys.exit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, help='Port on which the server will listen', required=False,
                        default=8080)
    parser.add_argument('--bind-address', '-b', type=str, help='IP address on which the server will listen',
                        required=False, default='127.0.0.1')
    return parser.parse_args()


def main():
    global server
    signal.signal(signal.SIGINT, sigint_handler)
    args = parse_args()
    server = socketserver.ThreadingTCPServer((args.bind_address, args.port), HttpHandler)
    server.daemon_threads = True
    server.allow_reuse_address = True
    try:
        while True:
            # sys.stdout.flush()
            server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
