from django.forms import ModelForm
from django import forms
from web.models import Video, Smartbook, Quiz
from ckeditor.widgets import CKEditorWidget


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = '__all__'


class SmartbookForm(ModelForm):
    class Meta:
        model = Smartbook
        fields = '__all__'


class SmartbookContentForm(ModelForm):
    content = forms.CharField(widget=CKEditorWidget, label='', required=True)

    class Meta:
        model = Smartbook
        fields = ['content']


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
