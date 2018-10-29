#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}

    def handle(self):
        line_str = self.rfile.read().decode('utf-8')
        linecontent = line_str.split()
        if linecontent[0] == 'REGISTER':
            usuario = linecontent[1].split(':')[-1]
            self.dic[usuario] = self.client_address[0]
            print(self.dic)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
