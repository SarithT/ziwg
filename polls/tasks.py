from celery import Celery
import os, shutil
import rpy2.robjects as ro
from django.conf import settings
from .scripts import CitationsMaker
from .scripts import LexemMaker
from .scripts import Parser
from django.core.mail import send_mail

app = Celery('tasks')
app.config_from_object('django.conf:settings')


@app.task
def run(path, n=40, model=1, browser=1, excel_name="", folder="", zip_file="",email_name=""):
    print("TASK STARTED")
    shutil.move(os.path.join(settings.MEDIA_ROOT, 'documents/' + str(excel_name)),
                os.path.join(settings.MEDIA_ROOT, 'documents/' + str(folder) + '/' + str(excel_name)))
    os.remove(os.path.join(settings.MEDIA_ROOT, 'documents/' + str(zip_file)))
    CitationsMaker.make(path, excel_name)
    LexemMaker.main(path)
    Parser.parser(path)
    rstring = """
    
        function(path, n, model, browser){
            setwd(path)
            options(java.parameters="-Xmx2g")
            library("rJava")
            library("mallet")
            library("dfrtopics")
            m <- model_dfr_documents(
                "outcsv/citations.tsv",
                "outcsv/wordcounts",
                n
            )
            if (model != 0) {
                # save model outputs
                write_mallet_model(m, output_dir="model")
            }
            if (browser != 0) {
                # create and save browser files
                export_browser_data(m, out_dir="browser", supporting_files=TRUE)
            }
        }
        """
    rr = ro.r(rstring)
    rr(path, n, model, browser)
    SendEmail('http://localhost:8000/media/documents/' + folder + '/browser/index.html', email_name)
    removeUseless(folder)


def SendEmail(link, email):
    print(link)
    subject='Cześć'
    massage='Tu jest twój link: ' + link
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject,massage,from_email,to_list,fail_silently=True)

def removeUseless(folder):
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'documents/' + str(folder) + '/in'))
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'outcsv'))
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT + '/documents/' + str(folder) + '/' + 'out'))

