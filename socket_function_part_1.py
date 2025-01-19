from operator import le
from tkinter.tix import Tree
from constants import *
import sys
import socket

def getTCPmessage(TCPSocket,size_want):
    packet = b""
    len_left = size_want - len(packet)
    flag_time_out = False
    
    while len_left != 0:
        message = TCPSocket.recv(len_left)
        if len(message) > 0 and not flag_time_out:
            flag_time_out = True
            TCPSocket.settimeout(None)
        packet += message
        len_left = size_want - len(packet)
    
        
    return packet

def send_chunk(TCPSocket,chunk_id , chunk):
    
    # chunk = chunk.encode()
    header_msg = f"{chunk_id} {len(chunk)}"
    header_msg = header_msg.ljust(headerSize).encode()
    
    TCPSocket.send(header_msg)
    
    message =  chunk

        
    TCPSocket.send(message)


def get_chunk(sock ,blocking = False,time_out = 0.1):

    chunk_id = -1
    chunk = ""
    try:
        sock.settimeout(time_out) 
        initial_header = getTCPmessage(sock,headerSize).decode()
        
        chunk_id,chunk_len = initial_header.split()
        chunk_id,chunk_len = int(chunk_id),int(chunk_len)
        
        chunk = getTCPmessage(sock,chunk_len)
    except socket.timeout:
        pass
        # #DEBUG print("It timed out")

    except socket.error as err:
        # #DEBUG print(f"Socket error happend {err}")
        return -2, ""

    except Exception as e:
        #DEBUG print("F")
        #DEBUG print(e)
        sys.exit(1)

    
    return chunk_id,chunk

def send_data(UDPSocket,destination_port,data):
        UDPSocket.sendto(data.encode(), (localIP, destination_port))

def get_data(UDPSocket ,blocking = False,time_out = 0.1):
    UDPSocket.setblocking(blocking)
    
    if not blocking:
        UDPSocket.settimeout(time_out)
    
    try:
        server_message = UDPSocket.recvfrom(bufferSize)[0].decode()
    except:
        server_message = exp_message
        # #DEBUG print("Timed out")
        
    if req_chunk in server_message or end_message in server_message:
        m, id =  server_message.split()
        return m, int(id)

    return server_message,0