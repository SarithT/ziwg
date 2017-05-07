from django import forms

from polls.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('Plik_zip', 'Plik_konfiguracyjny','Ilość_tematów','Email' )

