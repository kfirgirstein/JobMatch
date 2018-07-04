"""
Definition of forms.
"""
import json
from django import forms
from app.models import Questions_weights,Company,Question
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class RegistrtionForm(UserCreationForm):
    email = forms.EmailField(required=True,label=_("Email"),
                               widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder':'Email'}))
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    first_name = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Last Name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}),
                               help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_("Confirm Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm Password'}))

    class Meta:
        model= User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2')
    def save(self, commit = True):
        user= super(RegistrtionForm, self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CompanyForm(forms.Form):

    threshold = forms.IntegerField(
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Min Grade'}))
    num_of_clusters=1
    class Meta:
        model= Company
        fields=(
            'threshold'
            )

    def save(self,user,commit = True):
        try:
            company=Company()
            company.threshold=self.cleaned_data['threshold']
            company.name=user.username
            try:
               list =json.loads(self.data["questions"])
               company.num_of_questions= len(list)
            except:
                company.num_of_questions=10
            company.user= User.objects.get(pk=user.pk)
            if commit:
                company.save()
            return company
        except:
            raise AttributeError("invalid Parameters")
 

class SuperRegistrtionForm(UserCreationForm):
    email = forms.EmailField(required=True,label=_("Email"),
                               widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder':'Email'}))
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Company name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}),
                               help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_("Confirm Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm Password'}))
    class Meta:
        model= User
        fields=(
            'username',
            'email',
            'password1',
            'password2')
    def save(self, commit = True):
        user= super(SuperRegistrtionForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.is_superuser=True
        if commit:
            user.save()
        return user



