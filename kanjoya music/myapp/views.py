from django.http import HttpResponse
from django.template.loader import render_to_string
from myapp import models
from myapp.models import *
import myapp

import datetime

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
