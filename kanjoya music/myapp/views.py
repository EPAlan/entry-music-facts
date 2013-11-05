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
    danni = Kanjoyan.objects.get(id=1 )

    danniFacts = UserFact.objects.filter(kanjoyan=danni)   
    
    
    data = {'myFacts' : danniFacts, 'username' : danni }
    rendered = render_to_string('addFact.html', {'data': data})
    
    return HttpResponse(rendered)

def showTrivia(request):
    return HttpResponse('showTrivia')

# Create your views here.
