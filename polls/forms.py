from django import forms

from polls.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('zip_file', 'xml_file','your_email' )
