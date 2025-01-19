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
    
        
    return packet.decode()

def send_data(TCPSocket,data):
    
    # #DEBUG print(data)
    try:
        data = data.ljust(headerSize)

        TCPSocket.send(data.encode())
    except:
        print("Done Socket Closed")


def get_data(sock ,blocking = False,time_out = 0.1):


    try:
        sock.settimeout(time_out) 
        server_message = getTCPmessage(sock,headerSize)
        # #DEBUG print(server_message)
    except:
        server_message = exp_message
        
    if req_chunk in server_message or end_message in server_message:
        m, id =  server_message.split()
        # #DEBUG print(f"{m} {id}")
        return m, int(id)

    return server_message.strip(),0

def send_chunk(UDPSocket,destination_port,chunk_id , chunk):
    
    header_msg = f"{chunk_id} {len(chunk)}"
    header_msg = header_msg.ljust(headerSize).encode()
    
    # #DEBUG print(f"Header Sent: {header_msg} Chunk is {chunk[:10]}")
    
    UDPSocket.sendto(header_msg, (localIP, destination_port))
    
    
    UDPSocket.sendto(chunk, (localIP, destination_port))

def get_chunk(UDPSocket ,blocking = False,time_out = 0.1):
    UDPSocket.setblocking(blocking)
    
    if not blocking:
        UDPSocket.settimeout(time_out)
    
    chunk_id = -1
    chunk = ""
    try:
        initial_header = UDPSocket.recvfrom(headerSize)[0].decode()
        
        # #DEBUG print(initial_header)
        
        chunk_id,chunk_len = initial_header.split()
        chunk_id,chunk_len = int(chunk_id),int(chunk_len)
        
        chunk = UDPSocket.recvfrom(chunk_len)[0]
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    