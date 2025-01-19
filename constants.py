n = 5
cache_size = n

data_file = "A2_small_file.txt"
localIP     = "127.0.0.1"



chunkSize  = 1024
headerSize = 40
delimSize = 0
bufferSize = chunkSize + headerSize

data_for_chunk_count =  ""
with open(data_file, 'rb') as f:
    data_for_chunk_count = f.read()

chunk_count = len(data_for_chunk_count) //chunkSize

if  len(data_for_chunk_count)  % chunkSize != 0:
    chunk_count += 1

del data_for_chunk_count


end_message = "Done_quit"
giving_chunk = "SendigChun"
skip_mesaage = "Skip_Mess"
req_chunk = "Req_Chun"

exp_message = "Pack_Exp"


port   = 16060

server_tcp = port
port += 1


server_udp_ports = [i for i in range(port,port + n)]
port += n

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n

