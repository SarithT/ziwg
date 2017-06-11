from django import forms

from polls.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('Nazwa_korpusu', 'Ilosc_tematow', 'Autor','Email', 'Opis_korpusu', 'Plik_zip', 'Plik_konfiguracyjny')

