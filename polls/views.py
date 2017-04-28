from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import DocumentForm
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
import mimetypes
from django.conf import settings
import os

# Create your views here.


def upload_content(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('thanks/')
    else:
        form = DocumentForm()

    return render(request,'main-page.html',{'form':form})

def thanks(request):
    return render(request, 'thanks.html')









# def download(request):
#     path_to_file = os.path.join(settings.MEDIA_ROOT, 'template.xlsx')
#     file = open(path_to_file,'rb')
#     print(path_to_file)
#     wrapper = FileWrapper(file)
#     response = HttpResponse(wrapper, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('template.xlsx')
#     response['X-Sendfile'] = smart_str(path_to_file)
#     return response



