import socket
import mp3play
from hipchat import HipChat
import time
import random
from os import path

# server config
HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port

# hipchat config
ROOM_ID = 90507
HIPCHAT_API_TOKEN = 'a864d83d6221ad09861b690109a9f7'

# set up server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# set up hipchat
hipster = HipChat(token=HIPCHAT_API_TOKEN)

def playSongForName(name):
    songsByName = {
        'alex':     ['baba-yetu-short.mp3'],
        'ara':      ['rocky-short.mp3'],
        'angela':   ['conga-short.mp3'],
        'arsineh':  ['black-betty-short.mp3'],
        'bobby':    ['black-keyes-short.mp3'],
        'colette':  ['coco-de-rasta-short.mp3'],
        'cole':     ['super-mario-bros-short.mp3', 'super-mario-bros-short.mp3', 'super-mario-bros-short.mp3', 'super-mario-bros-short.mp3', 'raidersmarch-short.mp3'],
        'erik':     ['im-not-that-girl-short.mp3'],
        'joey':     ['talking-head-short.mp3'],
        'justin':   ['austin-powers-short.mp3'],
        'kate':     ['the-man-in-me-short.mp3'],
        'kumar':    ['give-up-the-funk-short.mp3'],
        'loren':    ['circle-of-life-short.mp3', 'good-morning-short.mp3', 'smooth-criminal-short.mp3', 'hard-victory-short.mp3', 'here-comes-the-sun-short.mp3'],
        'moritz':   ['peponi-short.mp3'],
        'mt':       ['boogie-on-reggae-woman-short.mp3'],
        'neil':     ['chariots-of-fire-short.mp3'],
        'rohan':    ['cotton-eye-joe-short.mp3'],
        'ryan':     ['sexy-and-i-know-it-short.mp3'],
        'soonlen':  ['another-world-short.mp3'],
        'stan':     ['baby-short.mp3'],
        'stephanie':['island-in-the-sun-short.mp3'],
        'sydni':    ['danger-zone-short.mp3'],
        'todd':     ['night-moves-short.mp3'],
        'tracy':    ['super-bass-short.mp3', 'gangnam-style-short.mp3'],
        'guest':    ['the-final-countdown-short.mp3']
    }

    goodbye_songs = [
        'so-long-farewell-short.mp3',
        'so-long-short.mp3',
        'heighho-short.mp3',
        'time-to-say-goodbye-short.mp3',
        'see-you-later-alligator-short.mp3',
        'i-hope-tomorrow-is-like-today-short.mp3',
        'home-short.mp3',
        'gone-short.mp3',
        'already-gone-short.mp3',
        'on-my-way-home-short.mp3',
        'na-na-hey-hey-short.mp3',
        'super-mario-bros-stage-clear.mp3'
    ]

    if time.localtime().tm_hour >= 16:
        filename = random.choice(goodbye_songs)
    else:
        if not songsByName.has_key(name):
            name = 'guest'
        songs = songsByName[name]
        filename = songs[time.localtime().tm_wday % len(songs)]

    print 'Playing song %s for %s' % (filename, name)    
    clip = mp3play.load(path.join('songs', filename))
    clip.play()

    time.sleep(clip.seconds())
    clip.stop()

def sendHipChatNotificationForName(name):
    if time.localtime().tm_hour >= 16:
        message = '(%s) has left the house.' % (name)
    else:
        message = '(%s) has entered the house.' % (name)
    hipster.method('rooms/message', method='POST', parameters={'room_id': ROOM_ID, 'from': 'The Announcer', 'message': message})

print "Listening on %s:%s" % (HOST, PORT)
while True:
    conn, addr = s.accept()
    print 'Received connection from ', addr
    while 1:
        data = conn.recv(1024)
        if not data: break

        sendHipChatNotificationForName(data)
        playSongForName(data)
        conn.send(data)
    print 'Closing connection'
    conn.close()
