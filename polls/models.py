from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    Plik_zip = models.FileField(upload_to='documents/')
    Plik_konfiguracyjny = models.FileField(upload_to='documents/')
    Ilość_tematów = models.SmallIntegerField()
    Email = models.EmailField(max_length=254)
    uploaded_at = models.DateTimeField(auto_now_add=True)
