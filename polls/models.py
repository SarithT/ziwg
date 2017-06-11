# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals
from django.core.validators import FileExtensionValidator

from django.db import models


class Document(models.Model):
    Nazwa_korpusu = models.CharField(max_length=100, null = True, blank = False)
    Autor = models.CharField(max_length=50, null = True, blank = False)
    Opis_korpusu = models.CharField(max_length=2000, null = True, blank = False)
    Plik_zip = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions="zip",message="Plik musi miec rozszerzenie .zip",code="zly rodzaj pliku")])
    Plik_konfiguracyjny = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions="xlsx, xls",message="Plik musi miec rozszerzenie .xls lub .xlsx",code="zly rodzaj pliku")])
    Ilosc_tematow = models.SmallIntegerField()
    Email = models.EmailField(max_length=254)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
