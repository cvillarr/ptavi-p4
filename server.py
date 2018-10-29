#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}

    def usuarios_expires(self):
        user_expired = []
        for usuario in self.dic:
            time_inicio = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(time.time()))
            if time_inicio >= self.dic[usuario][1]['expires']:
                user_expired.append(usuario)
        for usuario in user_expired:
            del(self.dic[usuario])
        print(user_expired)

    def register2json(self):
        ficherojson = open('registered.json', 'w')
        cod_json = json.dumps(self.dic)
        ficherojson.write(cod_json)
        ficherojson.close()

    def handle(self):
        line_str = self.rfile.read().decode('utf-8')
        linecontent = line_str.split()
        self.wfile.write("SIP/2.0 200 OK\r\n\r\n".encode('UTF-8'))
        if linecontent[0] == 'REGISTER':
            usuario = linecontent[1].split(':')[-1]
            IP = self.client_address[0]
        if linecontent[3] == 'Expires:':
            expires = time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.gmtime(time.time() +
                                                int(linecontent[4])))
            self.dic[usuario] = [{'address': IP}, {'expires': expires}]
        self.usuarios_expires()
        self.register2json()


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
