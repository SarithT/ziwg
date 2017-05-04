from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import DocumentForm
from django.http import JsonResponse
import zipfile
import json
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import mimetypes
from django.conf import settings
import os

# Create your views here.


def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        file = request.FILES['Plik_zip']
        if form.is_valid():
            unzipping_file(file)
            form.save()
            os.remove(os.path.join(settings.MEDIA_ROOT, 'documents/'+str(file)))
            return HttpResponseRedirect('')
    else:
        form = DocumentForm()
    return render(request, 'new.html', {'form':form})


def new(request):
    return render(request, 'new.html')

def unzipping_file(name):
    with zipfile.ZipFile(name, "r") as z:
        z.extractall("media/documents")

def index(request):
    return render(request, 'index.html')

def all(request):
    return render(request, 'all.html')





# def download(request):
#     path_to_file = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')
#     file = open(path_to_file,'rb')
#     print(path_to_file)
#     wrapper = FileWrapper(file)
#     response = HttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('template.xlsx')
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response



