import socket
import sys

inputFile = open("PROJI-HNS.txt","r")
outputFile = open("RESOLVED.txt","w")

def sendRSRequest(sock,domain_server):
    sock.send(domain_server)
    data = sock.recv(1024)
    return data

def sendTSRequest(info,tsHostName,port):
    ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts_socket.connect((tsHostName,port))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[Client]: TS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    ts_socket.send(domain_server)
    data = ts_socket.recv(1024)

    output = data.split(' ')
    flag = output[2]
    
    if flag == 'NS':
        outputFile.write(output[0] + ' - Error: HOST NOT FOUND' + '\n')
    else: 
        outputFile.write(data + '\n')
    ts_socket.close()
    return

if __name__ == "__main__":
    # Get input arguments
    rsHostName = socket.gethostbyname(sys.argv[1])
    rsPort = int(sys.argv[2])
    tsPort = int(sys.argv[3])

    # Create socket for RS
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[Client]: RS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    sock.connect((rsHostName,rsPort))

    # Get domain server names from input file
    for line in inputFile:
        domain_server = line.rstrip()
        data = sendRSRequest(sock,domain_server)
        data_arr = data.split(" ")
        flag = data_arr[2]

        # If domain_server not found in RS, then try in TS
        if flag == 'NS':
            tsHostName = socket.gethostbyname(data_arr[0])
            sendTSRequest(domain_server,tsHostName,tsPort)
        else:
            outputFile.write(data + '\n')

    inputFile.close()
    outputFile.close()
    sock.close()

