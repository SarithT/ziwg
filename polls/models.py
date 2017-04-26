from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    zip_file = models.FileField(upload_to='documents/')
    xml_file = models.FileField(upload_to='documents/')
    your_email = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
