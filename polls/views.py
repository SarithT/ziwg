# This Python file uses the following encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from django.db import models

from wsgiref.util import FileWrapper

from .forms import DocumentForm

from .scripts import CitationsMaker
from .scripts import LexemMaker
from .scripts import Parser
import rpy2.robjects as ro
from .tasks import run

from .models import Document
import zipfile
import os, shutil
import string
import random
import threading

# Create your views here.

#zapisanie danych na serwerze + dzialanie
def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            folder = id_generator()

            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder)))
            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'outcsv'))
            os.mkdir(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'out'))
            path_to_folder = os.path.join(settings.MEDIA_ROOT, 'documents/' + folder + '/')

            zip_file = request.FILES['Plik_zip']
            excel_name = request.FILES['Plik_konfiguracyjny']
            email = request.POST['Email']
            number_of_topics = request.POST['Ilosc_tematow']
            form.save()
            unzipping_file(zip_file, folder)

            # shutil.move(os.path.join(settings.MEDIA_ROOT, 'documents/'+str(excel_name)),os.path.join(settings.MEDIA_ROOT, 'documents/'+str(folder)+'/'+str(excel_name)))
            # os.remove(os.path.join(settings.MEDIA_ROOT, 'documents/'+str(zip_file)))
            # CitationsMaker.make(path_to_folder,excel_name)
            # LexemMaker.main(path_to_folder)
            # Parser.parser(path_to_folder)

            run.delay(path_to_folder,number_of_topics,1,1,excel_name,folder,zip_file,email)

            # rcall(path_to_folder,number_of_topics,1,1)
            # shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'documents/' + str(folder) + '/in'))
            # shutil.rmtree(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'outcsv'))
            # shutil.rmtree(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'out'))


            # SendEmail('http://localhost:8000/media/documents/'+folder+'/browser/index.html',email)
            return HttpResponseRedirect('')
    else:
        form = DocumentForm()
    return render(request, 'new.html', {'form':form})


# def rcall(path=os.getcwd(), n=40, model=1, browser=1):
#     rstring = """
#
# 	function(path, n, model, browser){
# 		setwd(path)
# 		options(java.parameters="-Xmx2g")
# 		library("rJava")
# 		library("mallet")
# 		library("dfrtopics")
# 		m <- model_dfr_documents(
# 			"outcsv/citations.tsv",
# 			"outcsv/wordcounts",
# 			n
# 		)
# 		if (model != 0) {
# 			# save model outputs
# 			write_mallet_model(m, output_dir="model")
# 		}
# 		if (browser != 0) {
# 			# create and save browser files
# 			export_browser_data(m, out_dir="browser", supporting_files=TRUE)
# 		}
# 	}
# 	"""
#     rr = ro.r(rstring)
#     rr(path, n, model, browser)


#generuje nazwe folderu
def id_generator(size=10, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#odpakowanie plików
def unzipping_file(name, folder_name):
    with zipfile.ZipFile(name, "r") as z:
        z.extractall(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder_name)))

#Wysylanie maila
# def SendEmail(link, email):
#     print(link)
#     subject='Cześć'
#     massage='Tu jest twój link: ' + link
#     from_email = settings.EMAIL_HOST_USER
#     to_list = [email]
#     send_mail(subject,massage,from_email,to_list,fail_silently=True)


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



