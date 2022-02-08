import socket
import sys

if __name__ == "__main__":
    DNS_Table = {}
    # Create socket
    try:
        rs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[RS]: RS Server socket created")
    except socket.error as err:
        print("socket open error: ()\n".format(err))
        exit()

    # Get input port
    rsListenPort = int(sys.argv[1])
    tsInput = socket.gethostbyname(sys.argv[2])
    rs.bind(('',rsListenPort))
    rs.listen(1)

    #Open DNSRS file and place info inside of DNS_table
    f = open("PROJI-DNSRS.txt","r")
    #foundTsHost = False
        
    for line in f:
        arr = line.strip().split(' ')
        dns,ip,flag = arr

        if flag != 'NS':
            DNS_Table[dns.lower()] = ip

    tsHostName = tsInput.lower() + " - NS"
    f.close()

    while True:
        sockid, addr = rs.accept()

        while True:
            data = sockid.recv(1024)
            if not data:
                break
            
            data = data.lower()

            if data in DNS_Table:
                #Found server
                sockid.send(data + " " + DNS_Table[data] + ' A')
            else:
                # Server not found, send back ts host name
                sockid.send(tsHostName)
            
    rs.close()
    
