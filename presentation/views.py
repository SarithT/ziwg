from django.shortcuts import render
from django.http import HttpResponseRedirect
from polls.models import Document

def index(request):
    path = request.get_full_path()
    split_path = path.split('/')
    korpus = Document.objects.get(id=split_path[2])
    return render(request, 'prez.html', {'korpus': korpus})

def setPublic(request):
    path = request.get_full_path()
    split_path = path.split('/')
    korpus = Document.objects.get(id=split_path[3])
    korpus.public = True
    korpus.save()
    return HttpResponseRedirect("/presentation/"+str(korpus.id))