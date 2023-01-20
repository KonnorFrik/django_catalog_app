from django import forms
from . import models
from . import validators


class RegistrationLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", max_length=150, widget=forms.PasswordInput)


class AnyFileForm(forms.ModelForm):
    class Meta:
        model = models.AnyFile
        fields = ['title', 'file']


class TextNoteForm(forms.Form):
    txt_title = forms.CharField(label="Title", max_length=25, required=False, validators=[validators.text_note_form_title_validation])
    txt_text = forms.CharField(label='Text', max_length=250, help_text="Maximum 250 symbols", widget=forms.Textarea)


class UserNoteForm(forms.Form):
    note_title = forms.CharField(label='Title For Note', max_length=100)
    note_description = forms.CharField(label="Description for note", max_length=300, widget=forms.Textarea, validators=[validators.user_note_form_description_validation])

    # file_form = AnyFileForm()
