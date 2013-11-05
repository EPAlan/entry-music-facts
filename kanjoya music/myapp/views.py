from django.http import HttpResponse
from django.template.loader import render_to_string

import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def addFact(request):
    rendered = render_to_string('addFact.html', {'data': 'data'})
    return HttpResponse(rendered)

def showTrivia(request):
    return HttpResponse('showTrivia')

# Create your views here.
