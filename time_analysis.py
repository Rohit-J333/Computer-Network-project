
import subprocess
import threading
import time
import os
import subprocess


for n in range(100,1100,10):
    constants_file = f'''n = 5
cache_size = {n}

data_file = "A2_large_small_file.txt"
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


port   = 15880

server_tcp = port
port += 1


server_udp_ports = [i for i in range(port,port + n)]
port += n

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n

'''   

    with open("constants.py", 'w') as f:
        f.write(constants_file)
        
    def run_s():
        cwd = os.path.join(os.getcwd(), "2020CS10342_server_part_2.py")
        os.system('{} {}'.format('python', "2020CS10342_server_part_2.py"))
        # time.sleep(360)

        # os.system('./2020CS10342_server.py')
        


    def run_c():
        cwd = os.path.join(os.getcwd(), "2020CS10342_client.py")
        os.system('{} {}'.format('python', f"2020CS10342_client_part_2.py"))
        # time.sleep(360)
        
        # os.system('./2020CS10342_client.py')


    print(f"Current n = {n}")

    # proc1 = subprocess.call(['python -u "/home/higgsboson/Codes/Sem 5/334/Assignment 2/2020CS10342_server.py"'], shell=True)
    # time.sleep(1)
    # proc2 = subprocess.call(['python -u "/home/higgsboson/Codes/Sem 5/334/Assignment 2/2020CS10342_client.py"'], shell=True)
    
    # time.sleep(360)
    # print()
    # print()
    # print()
    # print()
    # print()
    # print()
    # proc1.terminate()
    # proc2.terminate()

    t1 = threading.Thread(target=run_s,args=[])
    t1.start()
    time.sleep(1)
    t2 = threading.Thread(target=run_c,args=[])
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"Done with n = {n}")
    
    