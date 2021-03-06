#!/usr/bin/env python

'''
#############################################################################
#                                                                           #
#   Client.py                                                               #
#   Copyright (C) 2013 linuxknow                                            #
#   linuxknow [at] gmail dot com                                            #
#   This program is free software: you can redistribute it and/or modify    #
#   it under the terms of the GNU General Public License as published by    #
#   the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                     #
#                                                                           #
#   This program is distributed in the hope that it will be useful,         #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>    #
#                                                                           #
#############################################################################
'''


import socket
import sys, getopt
import os
from sendfile import sendfile

class ClientAnotes(object):
    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 24837
        self.TCP_PORTFILE = 24839
        self.BUFFER_SIZE = 8048
        self.MESSAGE = ""
        self.FILE = None
        self.nombreAdjunto = None
        self.hostname=""

    def setAttach(self,nombre,nombrearchivo):
        self.FILE = nombre
        self.nombreAdjunto = nombrearchivo
    def setPortFile(self,port):
        self.TCP_PORTFILE=port

    def send(self):
         try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TCP_IP, self.TCP_PORT))
                protocolo="%s\n" % (self.getHostName())
                s.send(protocolo)
                s.send(str(self.MESSAGE))
                s.close()
                return 0
         except:
                e = sys.exc_info()[0]
                print( "<p>Error al enviar mensaje: %s</p>" % e )
                return 1

    def sendFile(self):
         try:
                
                file_handle = open(self.FILE, "rb")
                #blocksize = os.path.getsize(self.FILE)
                #offset = 0
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TCP_IP, self.TCP_PORTFILE))
                s.send(self.nombreAdjunto)
                s.recv(self.BUFFER_SIZE)
                while True:
                    #sent = sendfile(s.fileno(), file_handle.fileno(), offset, blocksize)
                    #print "valor enviado con sendfile: %s\n" % sent 
                    #if sent == 0:
                    #    break
                    #offset += sent
                    data = file_handle.read(self.BUFFER_SIZE)
                    if not data:
                        break  # EOF
                    s.send(data)

                #print "Cerrando client..."
                file_handle.close()
                s.close()
                return 0
         except:
                e = sys.exc_info()[0]
                print( "<p>Error al enviar archivo:  %s</p>" % e )
                return 1
               
    def setPort(self,port):
        self.TCP_PORT=port

    def setServer(self,ip):
        self.TCP_IP=ip

    def setMessage(self,m):
        self.MESSAGE = m
    def setHostName(self,host):
        self.hostname=host
    def getHostName(self):
        return self.hostname
        

def main():
   ip = ''
   puerto = ''
   mensaje = ''
   try:
      if len(sys.argv) < 3:
          print 'Only accept three argument atnotes -ip client-server -p port -m message'
          return 2
      opts, args = getopt.getopt(sys.argv[1:],"hs:p:m:")

   except getopt.GetoptError:
      print 'atnotes.py -s <ip> -p <puerto> -m <message>'
      return 2
   for opt, arg in opts:
      if opt == '-h':
         print 'atnotes.py -s <ip> -p <puerto> -m <message>'
         return 1
      elif opt in ("-s"):
         ip = arg
      elif opt in ("-p", "--puerto"):
         puerto = arg
      elif opt in ("-m", "--message"):
         mensaje = arg

   ''' 
   print 'ip is %s' % ip
   print 'Name is %s' % puerto
   print 'Message is %s' % mensaje
   '''
   client = ClientAnotes();
   client.setPort(int(puerto))
   client.setServer(ip)
   client.setMessage(mensaje)
   client.send()
   return 0
   
   
if __name__ == '__main__':
    status = main()
    sys.exit(status)
