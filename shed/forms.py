#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from datetime import datetime
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from shed.models import Project, Task, Comment, User
from shed.service import get_current_time, time_zon


class RegisterUserForm(UserCreationForm):
    """форма регистрации"""
    first_name = forms.CharField(label='Имя', widget= forms.TextInput())
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())
    email = forms.EmailField(max_length=150, label='email', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('first_name','username', 'password1', 'password2', 'email')


class LoginUserForm(AuthenticationForm):
    """форма авторизации"""

    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class CommentForm(forms.ModelForm):
    """Для написания комментария"""
    class Meta:
        model = Comment
        fields = ['text',]

    def clean_completion_date(self):
        completion_date = self.cleaned_data['text']
        if completion_date==None:
            raise ValidationError('Введите комментарий')
        return completion_date


class LoginUserForm(AuthenticationForm):
    """форма авторизации"""

    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class ProjectCreateForm(forms.ModelForm):
    """Для создания изменения и удаления проекта"""

    class Meta:
        model = Project
        fields = ['name', 'description', 'user', 'completion_date', 'state']
        widgets = {
        'completion_date': forms.DateInput(attrs={'type': 'date'}),
        'user': forms.CheckboxSelectMultiple()
    }

    def clean_name(self):
        """пользовательсткая валидация"""
        name = self.cleaned_data['name']
        if len(name)==0:
            raise ValidationError('Название проекта не может быть пустым полем')
        return name

    def clean_user(self):
        user = self.cleaned_data['user']
        if len(user)==0:
            raise ValidationError('Добавьте участников проекта')
        return user

    def clean_completion_date(self):
        completion_date = time_zon(self.cleaned_data['completion_date'])
        if completion_date!=None:
            if completion_date.date()<get_current_time().date():
                raise ValidationError('Нельзя вводить дату из прошлого!')
        return completion_date


class TaskUpdateStateForm(forms.ModelForm):
    """Для изменения статуса задачи"""

    class Meta:
        model = Task
        fields = ['state']


class TaskCreateForm(forms.ModelForm):
    """для создания задачи"""

    def __init__(self, *args, **kwargs):
        """переопределили"""
        proj_pk = kwargs.pop('pk', None)
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        proj = Project.objects.get(pk=proj_pk)
        self.fields['executor'] = forms.ModelChoiceField(queryset=proj.user.all(), required=False, label='Исполнитель', empty_label='Выберите исполнителя')


    class Meta:
        model = Task
        fields = ['name', 'description', 'completion_date', 'state','executor']
        widgets = {
            'executor': forms.RadioSelect(),
            'completion_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': "datetime-local"}, format='%Y-%m-%dT%I:%M'),
        }

    def clean_name(self):
        """пользовательсткая валидация"""
        name = self.cleaned_data['name']
        if len(name)==0:
            raise ValidationError('Название задачи не может быть пустым полем')
        return name

    def clean_executor(self):
        data = self.cleaned_data
        executor = data['executor']
        if executor==None or executor=='Выберите исполнителя':
            raise ValidationError('Выберите исполнителя вашей задачи!')
        return executor

    def clean_completion_date(self):
        completion_date = self.cleaned_data['completion_date']
        date_rez = time_zon(self.cleaned_data['completion_date'])
        if completion_date!=None:
            if date_rez<get_current_time():
                raise ValidationError('Нельзя вводить дату из прошлого!')
        return completion_date