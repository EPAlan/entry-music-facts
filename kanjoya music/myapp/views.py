from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render

from myapp import models
from myapp.models import *
import myapp
import random
import datetime

def index(request):
    x = myapp.models.Kanjoyan(username = 'danni', id = 1 )
    y = myapp.models.Kanjoyan(username = 'alan', id = 2 )
    user_list = []
    user_list.append(x)
    user_list.append(y)
    context = {'user_list': user_list}

    return render(request, 'index.html', context)

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def addFact(request):
    crap = request.POST
    try:
        user_id = crap['user_id']
    except Exception:
        user_id = 1
        #TODO REDIRECT TO LOGIN

    danni = Kanjoyan.objects.get(id=user_id)

    danniFacts = UserFact.objects.filter(kanjoyan=danni)   
    
    
    data = {'myFacts' : danniFacts, 'username' : danni.username, 'userId' : user_id }
    rendered = render_to_string('addFact.html', {'data': data})
    final = "<div class='everything'>" + rendered + "</div>";
    return HttpResponse(final)

def trivia(request):
    final = 'shitTrivia'
    randomFact = getRandomFact()
    factText = randomFact.fact.text

    randomUsers = getRandomUsers(5)
    randomUsers.append(randomFact.kanjoyan)
    random.shuffle(randomUsers)
    randomUsers = list(set(randomUsers))

    answer = randomFact.kanjoyan

    data = {'answer' : answer, 'kanjoyans' : randomUsers, 'randomFact' : randomFact }
    rendered = render_to_string('randomFact.html', {'data': data})
    
    return HttpResponse(rendered)

def getRandomFact():
    allFacts = list(UserFact.objects.all())
    random.shuffle(allFacts)
    return allFacts[0]

def getRandomUsers(limit):
    allKanjoyans = list(Kanjoyan.objects.all())
    random.shuffle(allKanjoyans)
    return allKanjoyans[:limit]

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

    final = "<div class='singleFact'>" + newUserFact.__unicode__() + "</div>";
    return HttpResponse(final)

def showTrivia(request):
    return HttpResponse('showTrivia')

# Create your views here.
