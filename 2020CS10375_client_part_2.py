from re import T
from statistics import mean
from constants import *
import socket
from LRU import  LRU
import threading

from tqdm import tqdm

from socket_function_part_2 import *
import hashlib
import time

import random
import matplotlib.pyplot as plt




lock = threading.Lock()


class Client:
    def __init__(self,index):
        self.index = index
        self.chunks_not_with_me = [i for i in range(chunk_count)]
        self.data_with_me = ["" for _ in range(chunk_count)]
        
        self.TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.TCPSocket.bind((localIP, tcp_client_ports[index]))
        self.TCPSocket.connect((localIP,server_tcp))
        
        self.TCPSocket.settimeout(10)
        
        self.am_i_done = False
        
        self.p_bar = tqdm(range(chunk_count),leave=True,desc=f"Client {index}",unit="Chunks",colour="#00ff00")
        
        
        
        
        
        
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((localIP,udp_client_ports[index]))
        
    def get_init_data(self):
        while True:
            id, chunk = get_chunk(self.UDPSocket)

            if id == -2:
                break
            
            self.p_bar.update(1)
            
            print(id)
            self.data_with_me[id] = chunk
            self.chunks_not_with_me.remove(id)
            
        #DEBUG print(f"Got initial Chunks to {self.index} {chunk_count - len(self.chunks_not_with_me)}")
    
    def client_fetch(self):
        while not self.am_i_done:
            msg_to_send = f"{end_message} {self.index}"
        
            if len(self.chunks_not_with_me)!= 0 :
                req_for = random.choice(self.chunks_not_with_me[:min(len(self.chunks_not_with_me), n//2)])
                msg_to_send = f"{req_chunk} {req_for}"
            
            send_data(self.TCPSocket,msg_to_send)
        
            if end_message in msg_to_send:
                time.sleep(3)
              
            # #DEBUG print(msg_to_send)      
                
            chunk_id, chunk = get_chunk(self.UDPSocket, False)      
            
            if chunk_id == -2:
                break
            elif chunk_id == -1:
                pass
            elif chunk == "":
                pass
                #DEBUG print("Kuch nhi aaya")
            elif chunk_id in self.chunks_not_with_me:
                #DEBUG print(f"Got {chunk_id}: {chunk[:5]}")
                self.p_bar.update(1)

                
                self.data_with_me[chunk_id] = chunk
                self.chunks_not_with_me.remove(chunk_id)

    def client_send(self):
        while True:
            message, id = get_data(self.TCPSocket)
            
            if req_chunk in message:
                if id not in self.chunks_not_with_me:  
                        send_data(self.TCPSocket,giving_chunk)
                        send_chunk(self.UDPSocket,server_udp_ports[self.index],id,self.data_with_me[id])
             
            elif end_message in message:
                
                    self.am_i_done = True
                    self.TCPSocket.shutdown(socket.SHUT_RDWR)
                    self.TCPSocket.close()           
                    
                    # print(f"{self.index} had an RTT of {mean(self.RTTS)}")

                    hash = hashlib.md5(b"".join(self.data_with_me)).hexdigest()
                    print(f"Client {self.index} says: Hash of file recieved:{hash}")
                    break
                    
   
clients = [Client(i) for i in range(n)]

for client in clients:             
    client.get_init_data()
    

start = time.time()

ts = []

for i,client in enumerate(clients):

    t1 = threading.Thread(target=client.client_fetch,args=[])
    t1.start()
    t2 = threading.Thread(target=client.client_send,args=[])
    t2.start()
    ts.append(t1)
    ts.append(t2)


    
for t in ts:
    t.join()


end = time.time()

with open("Part 2 Timing.txt", "a") as f:
    f.write(f"{n}, {end-start} \n")


