from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render

from myapp import models
from myapp.models import *
import myapp
import random
import datetime
from subprocess import Popen
import tempfile
import shutil
from hipchat import HipChat
import time
#import pyglet
import os
#import AVbin

# hipchat config
ROOM_ID = 90507
HIPCHAT_API_TOKEN = 'a864d83d6221ad09861b690109a9f7'
hipster = HipChat(token=HIPCHAT_API_TOKEN)

def sendHipChatNotificationForName(name):
    if time.localtime().tm_hour >= 16:
        message = '(%s) has left the house.' % (name)
    else:
        message = '(%s) has entered the house.' % (name)
    hipster.method('rooms/message', method='POST', parameters={'room_id': ROOM_ID, 'from': 'The Announcer', 'message': message})

def index(request):
    kanjoyans = list(Kanjoyan.objects.all())
    context = {'user_list': kanjoyans}
    return render(request, 'index.html', context)

def scoreboard(request):
    scores = list(Score.objects.all())
    ranked = sorted(scores, key=lambda Score: Score.score, reverse=True)
    rendered = render_to_string("scoreboard.html", {'scores' : ranked})
    return HttpResponse(rendered)

def visitor(request):
    filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/visitor.mp3'
    try:
        open(filename)
    except IOError:
        filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/default.mp3'
    playSong(filename)
    sendHipChatNotificationForName('Visitor')
    rendered = render_to_string('visitor.html')
    final = "<div class='everything'>" + rendered + "</div>";
    return HttpResponse(final)

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def getUserId(request):
    crap = request.POST
    try:
        user_id = crap['user_id']
    except Exception:
        user_id = 1
        #TODO REDIRECT TO LOGIN
    return user_id

def addFact(request, random_key):
    currentUser = Kanjoyan.objects.get(randomKey=random_key)
    userFacts = UserFact.objects.filter(kanjoyan=currentUser)
    user_id = currentUser.id
    
    data = {'myFacts' : userFacts, 'username' : currentUser.username, 'userId' : user_id }
    rendered = render_to_string('addFact.html', {'data': data})
    final = "<div class='everything'>" + rendered + "</div>";
    return HttpResponse(final)

def trivia(request, user_id):
    currentUser = Kanjoyan.objects.get(id=user_id)
    randomFact = getRandomFact()
    factText = randomFact.fact.text

    #randomUsers = getRandomUsers(6)
    #randomUsers.append(randomFact.kanjoyan)
    #random.shuffle(randomUsers)
    #randomUsers = list(set(randomUsers))

    randomUsers = getRandomUsersExcluding(5, randomFact.kanjoyan.id)
    randomUsers.append(randomFact.kanjoyan)
    random.shuffle(randomUsers)
    randomUsers = list(set(randomUsers))

    answer = randomFact.kanjoyan

    data = {'answer' : answer, 'kanjoyans' : randomUsers, 'randomFact' : randomFact, 'currentUser' : currentUser }
    rendered = render_to_string('randomFact.html', {'data': data})
    return HttpResponse(rendered)

def showAnswer(request):
    user_id = getUserId(request)
    currentUser = Kanjoyan.objects.get(id=user_id)
    crap = request.POST
    factId = crap['fact_id']
    fact = UserFact.objects.get(id=factId)
    success = crap['success']

    filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/' + currentUser.username + '.mp3'
    if (success == '1'):
        processScore(user_id)
    try:
        open(filename)
    except IOError:
        filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/default.mp3'
    if currentUser.username == 'Danni':
	limit = 15
    else:
        limit = 10

    playSong(filename, limit)
    sendHipChatNotificationForName(currentUser.username + filename)

	#filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/good-morning-short.mp3'
    	#song = pyglet.media.load(filename)
    	#song.play()
    	#pyglet.app.run()

    data = {'fact' : fact, 'success' : success, 'currentUser' : currentUser }
    rendered = render_to_string('showAnswer.html', {'data': data})
    return HttpResponse(rendered)

def playSong(filename, limit=10):
    cmd = 'mpg123 ' + str(limit) + ' ' + filename
    Popen(cmd, shell=True)


def uploadFileView(request, random_key):
    currentUser = Kanjoyan.objects.get(randomKey=random_key)
    rendered = render_to_string('navigation.html', { "randomKey" : random_key })
    rendered += render_to_string('uploadFile.html', {'currentUser' : currentUser})
    return HttpResponse(rendered)

def uploadPictureView(request, random_key):
    currentUser = Kanjoyan.objects.get(randomKey=random_key)
    rendered = render_to_string('navigation.html', { "randomKey" : random_key })
    rendered += render_to_string('uploadPicture.html', {'currentUser' : currentUser})
    return HttpResponse(rendered)

def uploadFile(request, user_id):
    filename = request.FILES['myfile']
    currentUser = Kanjoyan.objects.get(id=user_id)
    filepath = handle_uploaded_file(filename, currentUser)
    return HttpResponse(filepath)    

def handle_uploaded_file(source, currentUser):

    filename = os.path.dirname(os.path.realpath(__file__)) + '/static/songs/' + currentUser.username + '.mp3'
    with open(filename, 'wb+') as destination:
        for chunk in source.chunks():
            destination.write(chunk)
    return filename

def uploadPicture(request, user_id):
    filename = request.FILES['myfile']
    currentUser = Kanjoyan.objects.get(id=user_id)
    filepath = handle_uploaded_picture(filename, currentUser)
    return HttpResponse(filepath)    

def handle_uploaded_picture(source, currentUser):

    filename = os.path.dirname(os.path.realpath(__file__)) + '/static/images/' + currentUser.username + '.jpg'
    with open(filename, 'wb+') as destination:
        for chunk in source.chunks():
            destination.write(chunk)
    return filename

def getRandomFact():
    allFacts = list(UserFact.objects.all())
    random.shuffle(allFacts)
    return allFacts[0]

def getRandomUsers(limit):
    allKanjoyans = list(Kanjoyan.objects.all())
    random.shuffle(allKanjoyans)
    return allKanjoyans[:limit]

def getRandomUsersExcluding(limit, factUserId):
    theKanjoyans = list(Kanjoyan.objects.exclude(id=factUserId))
    random.shuffle(theKanjoyans)
    return theKanjoyans[:limit]

def ajaxAddFact(request):
    crap = request.POST
    userId = crap['user_id']
    fact = crap['new_fact']
    currentUser = Kanjoyan.objects.get(id=userId)

    try :
        existingFact = Fact.objects.get(text=fact)
        newUserFact = UserFact(fact=fact, kanjoyan=currentUser)
        newUserFact.save()
    except Exception:
        newFact = Fact(text=fact)
        newFact.save()
        newUserFact = UserFact(fact=newFact, kanjoyan=currentUser)
        newUserFact.save()

    final = "<div class='singleFact'>" + newUserFact.fact.text + "</div>";
    return HttpResponse(final)

def processScore(userId):
    currentUser = Kanjoyan.objects.get(id=userId)
    try:
        userScore = Score.objects.get(kanjoyan=currentUser)
        userScore.score += 1
        userScore.save()
    except Exception:
        userScore = Score(kanjoyan=currentUser, score=1)
        userScore.save()
    return userScore.score

def getUserScore(userId):
    currentUser = Kanjoyan.objects.get(id=userId)
    userScore = Score.objects.get(kanjoyan=currentUser)
    return userScore.score

    
 #Create your views here.
