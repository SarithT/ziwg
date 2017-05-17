from __future__ import unicode_literals

from django.db import models


class Document(models.Model):
    Nazwa_korpusu = models.CharField(max_length=100, null = True, blank = False)
    Autor = models.CharField(max_length=50, null = True, blank = False)
    Opis_korpusu = models.CharField(max_length=2000, null = True, blank = False)
    Plik_zip = models.FileField(upload_to='documents/')
    Plik_konfiguracyjny = models.FileField(upload_to='documents/')
    Ilość_tematów = models.SmallIntegerField()
    Email = models.EmailField(max_length=254)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

