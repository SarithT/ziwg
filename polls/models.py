from __future__ import unicode_literals
from django.core.validators import FileExtensionValidator

from django.db import models


class Document(models.Model):
    Nazwa_korpusu = models.CharField(max_length=100, null = True, blank = False)
    Autor = models.CharField(max_length=50, null = True, blank = False)
    Opis_korpusu = models.CharField(max_length=2000, null = True, blank = False)
    Plik_zip = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions="zip",message="Plik musi mieć rozszerzenie .zip",code="zły rodzaj pliku")])
    Plik_konfiguracyjny = models.FileField(upload_to='documents/',validators=[FileExtensionValidator(allowed_extensions="xlsx, xls",message="Plik musi mieć rozszerzenie .xls lub .xlsx",code="zły rodzaj pliku")])
    Ilość_tematów = models.SmallIntegerField()
    Email = models.EmailField(max_length=254)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
