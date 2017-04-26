from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DocumentForm
import zipfile

# Create your views here.


def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #content = request.FILES['content']
            #unzipped = zipfile.ZipFile(content,'r').extractall('.')
            #unzipped.save()
            form.save()
            return HttpResponseRedirect('thanks/')
    else:
        form = DocumentForm()

    return render(request,'main-page.html',{'form':form})

def thanks(request):
    return render(request, 'thanks.html')

def extractZip(fileName):
    zf = zipfile.ZipFile(fileName, 'r').extractall('.')




