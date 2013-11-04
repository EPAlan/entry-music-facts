import socket
import mp3play

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print "Listening on %s:%s" % (HOST, PORT)
while True:
    conn, addr = s.accept()
    print 'Received connetion from ', addr
    while 1:
        data = conn.recv(1024)
        if not data: break
        print data
        conn.send(data)
    print 'Closing connection'
    conn.close()
