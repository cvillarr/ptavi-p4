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

    def register2json(self):
        """
        Crea fichero json y almacena las direcciones"
        """
        ficherojson = open('registered.json', 'w')
        cod_json = json.dumps(self.dic)
        ficherojson.write(cod_json)
        ficherojson.close()

    def json2registered(self):
        """
        Comprueba si existe fichero json para poder seguir escribiendo en él
        """
        try:
            ficherojson = open('registered.json', 'r')
            self.dic = json.load(ficherojson)
        except FileNotFoundError:
            pass

    def usuarios_expires(self):
        """
        Comprueba si hay usuarios expirados y si los hay los elimina
        """
        user_expired = []
        for usuario in self.dic:
            time_inicio = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(time.time()))
            if time_inicio >= self.dic[usuario][1]['expires']:
                user_expired.append(usuario)
        for usuario in user_expired:
            del(self.dic[usuario])

    def handle(self):
        """
        Se encarga de actuar cuando recibe un REGISTER
        """
        line_str = self.rfile.read().decode('utf-8')
        linecontent = line_str.split()
        self.json2registered()

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
        self.wfile.write("SIP/2.0 200 OK\r\n\r\n".encode('UTF-8'))


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
