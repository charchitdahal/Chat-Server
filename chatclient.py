#!/usr/bin/env python
import socket
import os
import sys
import thread
import time
import json

server_ip = sys.argv[1]
server_port = 1134
username = sys.argv[2]
sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM )

def get_messages():
  global sock, username
  while True:
    data = None
    try:
      data, addr = sock.recvfrom( 1024, socket.MSG_DONTWAIT )
    except socket.error:

      time.sleep(0.01)
    if data:

      try:

        message = json.loads(data)

        if(message['username'] != username):
          msg_str = message['message']
        #else:
         # print "DUPLICATE"

        #if(message['username'] == username):
         # print "DUPLICATE USERNAME"

          if(message['username']):
            msg_str = message['username'] + ": " + msg_str

          #  print the message
          if len(message['message']) > 0:
            print msg_str
      except ValueError:
        print "error: can not retrive message"

def get_input():
  global sock, username
  try:
    while True:
      message = { "username" : username, "message" : raw_input().strip()}
      sock.sendto( json.dumps(message), (server_ip, int(server_port)) )

  except KeyboardInterrupt:
    print "bye"

thread.start_new_thread(get_input, ())
thread.start_new_thread(get_messages, ())

#  upon "connecting", send /join and /who to announce our arrival and get a list
#  of other people in the room
message = { "username" : username, "message" : "/join"}
sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
message = { "username" : username, "message" : "/who"}
sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
try:
  while 1:
    time.sleep(0.01)
except KeyboardInterrupt:
  print "bye"
  message = { "username" : username, "message" : "/bye"}
  sock.sendto( json.dumps(message), (server_ip, int(server_port)) )
  sys.exit(0)
