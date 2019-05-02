#!/usr/bin/env python
import socket
import time
import sys
import json

UDP_IP= sys.argv[1]
UDP_PORT= 1134

sock = socket.socket( socket.AF_INET,
                      socket.SOCK_DGRAM )

print "Chat Server Started On " +  str(UDP_PORT)

sock.bind( (UDP_IP,UDP_PORT) )

clients = []
names = []
list(set(clients))
list(set(names))


if len(clients) > 10:
    print " Chat Server Full"

def broadcast(data):
  global clients
  global names
  for client in clients:
      sock.sendto(data, client[1])


while True:
    data = None
    message = None
    try:
      # try to get a message on the socket
      data, addr = sock.recvfrom( 1024, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes



      message = json.loads(data)
      client = (message['username'], addr)
      name = (message['username'])

      if name not in names:
          names.append(name)




      #if user_name in names:
        #print "Username already taken"

      if client not in clients:
        clients.append(client)

    except socket.error:


      time.sleep(0.01)

    if data:

      try:

        #if (message['username'] == user_name):
         #  print "TESTING TESTING"
           #clients.remove(client)
        if name not in names:
            print "DUPLICATE USERNAME"

        if( message['message'].startswith("/join") ):

          outjson = {"username" : "server",\
            "message" : message['username'] + " joined the chat"}

          broadcast( json.dumps(outjson) )


        elif ( message['message'].startswith("/who") ):

          outjson = {"username" : "server",\
            "message" : "people in room: " + ', '.join([y[0] for y in clients])}

          sock.sendto( json.dumps(outjson), client[1] )


        elif ( message['message'].startswith("/bye") ):

          outjson = {"username" : "server",\
            "message" : message['username'] + " left the chat"}
          clients.remove(client)
          broadcast( json.dumps(outjson) )


        elif ( message['message'].startswith("/me") ):

          newmsg = message['username'] + message['message'][3:]
          outjson = {"username" : None,\
            "message" : newmsg}

          broadcast( json.dumps(outjson) )

        else:
          outjson = {"username" : message['username'],\
            "message" : message['message'] }
          broadcast( json.dumps(outjson) )

        print clients

      except ValueError:

        print "indecipherable json"
