#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys  #for exit
from random import randint
import datetime
#Establishes a UDP-socket
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print ('Misslyckades med att skapa socket. Felkod: ' + str(msg[0]) + ' , Felmeddelande : ' + msg[1])
    sys.exit();

port = 1234
#-----------------------------
#Global variables
show_time = ()
post_time = ()
host = ''
# Just a hacky way for the server to know who has connected
def tell_server_of_connection(playername, server):
    udp_socket.sendto(playername, (server,port))
    global host
    host = server

# Recieve the random generated position from the server
def recieve_position_and_object_from_server():
    msg, addr = udp_socket.recvfrom(1024)
    data = msg.split(',')
    obj = data[0]
    coord = data[1],data[2]
    global show_time
    show_time = datetime.datetime.strptime(data[3], '%Y-%m-%d %H:%M:%S.%f')
    while datetime.datetime.now() < show_time:
        pass
    return obj, coord

#Receive score and playernames
def score_user_receive():
    msg, addr = udp_socket.recvfrom(1024)
    data = msg.split(';')
    players = []
    scores = []
    for i in range(len(data)-1):
        p = data[i].split(',')
        players.append(p[0])
        scores.append(p[1])
    return players, scores, len(players)

def send_timestamp():
    global post_time
    global show_time
    post_time = datetime.datetime.now()
    diff_time = post_time - show_time
    udp_socket.sendto('[1,'+str(diff_time)+']', (host,port))

def recieive_nr_rounds():
    msg, addr = udp_socket.recvfrom(1024)
    return int(msg)

#def main():
#    tell_server_of_connection("sebbe",'130.243.197.82')
#    while True:
#       users, scores = score_user_receive()
        # recieve_position_and_object_from_server()
#        send_timestamp()
#    s.close
#if __name__ == "__main__":
#    main()
