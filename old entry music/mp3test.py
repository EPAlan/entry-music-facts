import mp3play

filename = 'cotton-eye-joe.mp3'
clip = mp3play.load(filename)

clip.play()

import time
time.sleep(min(2, clip.seconds()))
clip.stop()
