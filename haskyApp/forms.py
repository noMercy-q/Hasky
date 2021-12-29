from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets

from django.forms.widgets import PasswordInput
from .models import Answer, Question

class LoginForm(forms.Form):
    username = forms.CharField()
    #email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    password = forms.CharField(widget = forms.PasswordInput)    
    repeat_password = forms.CharField(widget = forms.PasswordInput)
    avatar = forms.ImageField(required = False)

    def clean(self):
        cdata = super().clean()
        if cdata['password'] != cdata['repeat_password']:
            self.add_error(None, "Passowords do not match!")
        return cdata

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'avatar']
    username = forms.CharField(disabled=True)
    avatar = forms.ImageField(required = False)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user

class QuestionForm(forms.ModelForm):
    #head = forms.CharField()
    #body = forms.CharField(widget = forms.Textarea)
    #tags = forms.CharField()
    
    class Meta:
        model = Question
        fields = ['head', 'body']
    tags = forms.CharField(required=False)

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['body']