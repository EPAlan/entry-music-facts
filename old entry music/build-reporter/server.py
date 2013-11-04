import socket
import mp3play
from hipchat import HipChat
import time
import random
from os import path

# server config
HOST = ''                 # Symbolic name meaning the local host
PORT = 50008              # Arbitrary non-privileged port

# hipchat config
ROOM_ID = 90507
HIPCHAT_API_TOKEN = 'a864d83d6221ad09861b690109a9f7'

# set up server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# set up hipchat
hipster = HipChat(token=HIPCHAT_API_TOKEN)

def playSong(filename):
    print 'Playing song %s' % (filename)    
    clip = mp3play.load(path.join('songs', filename))
    clip.play()

    time.sleep(clip.seconds())
    clip.stop()

print "Listening on %s:%s" % (HOST, PORT)
while True:
    conn, addr = s.accept()
    print 'Received connection from ', addr
    while 1:
        data = conn.recv(1024)
        if not data: break

        print data
        if data == 'unit tests failed':
            playSong('inception-short.mp3')

    print 'Closing connection'
    conn.close()
