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
import os, shutil
import string
import random
from .forms import DocumentForm
from .models import Document
from django.core.mail import send_mail

# Create your views here.


def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        folder = id_generator()
        zip_file = request.FILES['Plik_zip']
        excel_file = request.FILES['Plik_konfiguracyjny']
        email = request.POST['Email']
        print (email)
        if form.is_valid():
            form.save()
            unzipping_file(zip_file, folder)
            shutil.move(os.path.join(settings.MEDIA_ROOT, 'documents/'+str(excel_file)),os.path.join(settings.MEDIA_ROOT, 'documents/'+str(folder)+'/'+str(excel_file)))
            os.remove(os.path.join(settings.MEDIA_ROOT, 'documents/'+str(zip_file)))
            SendEmail('http://127.0.0.1:8000/media/documents/'+folder+'/index.html',email)
            return HttpResponseRedirect('')
    else:
        form = DocumentForm()
    return render(request, 'new.html', {'form':form})


def SendEmail(link, email):
    subject='Cześć'
    massage='Tu jest twój link: ' + link
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject,massage,from_email,to_list,fail_silently=True)


def new(request):
    return render(request, 'new.html')

def unzipping_file(name, folder_name):
    with zipfile.ZipFile(name, "r") as z:
        z.extractall("media/documents/"+str(folder_name))

def index(request):
    return render(request, 'index.html')

def all(request):
    return render(request, 'all.html')

def id_generator(size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




# def download(request):
#     path_to_file = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')
#     file = open(path_to_file,'rb')
#     print(path_to_file)
#     wrapper = FileWrapper(file)
#     response = HttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('template.xlsx')
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response



