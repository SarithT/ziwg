# This Python file uses the following encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from .forms import DocumentForm
from .tasks import run

from .models import Document
import zipfile
import os
import string
import random

# Create your views here.

#zapisanie danych na serwerze + dzialanie
def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            zip_file = request.FILES['Plik_zip']
            excel_name = request.FILES['Plik_konfiguracyjny']
            email = request.POST['Email']
            number_of_topics = request.POST['Ilość_tematów']
            saved_korpus = form.save()
            folder = saved_korpus.id

            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder)))
            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'outcsv'))
            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'out'))
            path_to_folder = os.path.join(settings.MEDIA_ROOT, 'documents/' + str(folder) + '/')


            unzipping_file(zip_file, folder)
            run.delay(path_to_folder,number_of_topics,1,1,excel_name,folder,zip_file,email)
            return render(request, 'thanks.html')
    else:
        form = DocumentForm()
    return render(request, 'new.html', {'form':form})

#generuje nazwe folderu
def id_generator(size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#odpakowanie plików
def unzipping_file(name, folder_name):
    with zipfile.ZipFile(name, "r") as z:
        z.extractall(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder_name)))


def index(request):
    last_ten = Document.objects.all().order_by('-id')[:10]
    indexTemplate = loader.get_template('index.html')
    context = {
        'last_ten': last_ten,
    }
    return HttpResponse(indexTemplate.render(context, request))

def all(request):
    allCorpuses = Document.objects.all().order_by('-id')
    allTemplate = loader.get_template('all.html')
    context = {
        'allCorpuses' : allCorpuses,
    }
    return HttpResponse(allTemplate.render(context, request))

def new(request):
    return render(request, 'new.html')


# def download(request):
#     path_to_file = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')
#     file = open(path_to_file,'rb')
#     print(path_to_file)
#     wrapper = FileWrapper(file)
#     response = HttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('template.xlsx')
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response



