
import numpy as np
from constants import *
import socket
from LRU import  LRU
import threading

import random

from socket_function_part_1 import *


import hashlib



lock = threading.Lock()

# Get initial data
data =  []
with open(data_file, 'rb') as f:
    while True:
        chunk = f.read(chunkSize)
        if not chunk: 
            break
        data.append(chunk)



# Initialise cache
cache = LRU()


# Get hash of data
hash = hashlib.md5(b"".join(data)).hexdigest()
#DEBUG print(hash)


#Deciding the split
oneton = np.arange(len(data))
np.random.shuffle(oneton)
index_to_split_chunk = np.array_split(oneton, n)


# Book keeping of client status
is_everyone_done = [False]*n
is_everyone_done_count = 0


#Made Connections
TCP_Clients = []
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPServerSocket.bind((localIP, server_tcp)) 
TCPServerSocket.listen(n)       

while len(TCP_Clients) < n:
    connectionSocket, addr = TCPServerSocket.accept()
    TCP_Clients.append(connectionSocket)

TCP_Clients = sorted(TCP_Clients, key=lambda x: x.getsockname()[1])



def make_server_t(index):
    global data
    global cache
    global is_everyone_done
    global is_everyone_done_count
    global lock
    

    TCPSocet = TCP_Clients[index]
    UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPSocket.bind((localIP,server_udp_ports[index]))
    
    UDPSocket_Client = udp_client_ports[index]

    
    #Sending initial chunks
    for id in index_to_split_chunk[index]:
        send_chunk(TCPSocet,id,data[id])
    send_chunk(TCPSocet,-2,end_message.encode())
    
    #DEBUG print(f"Sent initial Chunks to {index}: {len(index_to_split_chunk[index])}")

    #Main server loop
    while is_everyone_done_count != n:    

        message, id = get_data(UDPSocket)
        
        if skip_mesaage not in message:
            pass
            #DEBUG print(f"I got {message} {id}")


        if req_chunk in message:
            with lock:
                cache_message = cache.get(id)
                
            if cache_message  == "":
                #DEBUG print(req_chunk + " " + str(id))
                for udp_port in udp_client_ports:
                    if udp_port != UDPSocket_Client:
                        send_data(UDPSocket,udp_port, req_chunk + " " + str(id))
            else:
                #DEBUG print(f"Able to sen from cache {id} {cache_message[0:10]}")
                send_data(UDPSocket,UDPSocket_Client, giving_chunk)
                send_chunk(TCPSocet,id,cache_message)

            
        elif giving_chunk in message:
            with lock:
                chunk_id, chunk = get_chunk(TCPSocet)   
                #DEBUG print(f"Got chunk {chunk[0:10]}")   
                if chunk != "":
                    cache.put(chunk_id,chunk)
                
        elif end_message in message:
            with lock:
                if not is_everyone_done[index]:
                    is_everyone_done_count += 1
                is_everyone_done[index] = True
                
 
        elif skip_mesaage in message:
            pass
        elif exp_message in message:
            pass
                #DEBUG print(f" Client {index} did nothing ")
        else:
            pass
            #DEBUG print(f"Yeh konsa packet aagya {message} {id}")
            
            
    send_data(UDPSocket,UDPSocket_Client,f"{end_message} {index}")
    
    hash = hashlib.md5(b"".join(data)).hexdigest()
    print(f"Server thread {index} says: Hash of file sent:{hash}")
    
    
    
ts = []

for i in range(n):
    t = threading.Thread(target=make_server_t,args=[i])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()
    
    