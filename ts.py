import socket
import sys

if __name__ == "__main__":
    DNS_Table = {}
    # Create socket
    try:
        ts = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[TS]: TS Server socket created")
    except socket.error as err:
        print("socket open error: ()\n".format(err))
        exit()

    
    # Get input port
    tsListenPort = int(sys.argv[1])
    ts.bind(('',tsListenPort))
    ts.listen(1)

    #Open file and check for domain server
    f = open("PROJI-DNSTS.txt","r")
    for line in f:
        arr = line.strip().split(' ')
        dns,ip,flag = arr
        
        # Add lines from file to dns table
        DNS_Table[dns.lower()] = ip

    while True:
        sockid, addr = ts.accept()

        while True:
            data = sockid.recv(1024)
            if not data:
                break
            
            data = data.lower()
            if data in DNS_Table:
                sockid.send(data + " " + DNS_Table[data] + ' A') 
            else:
                sockid.send(data + ' - Error:HOST NOT FOUND')
            
    ts.close()
    
