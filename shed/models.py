#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

from shed.service import word_form, time_zon


class ChoicesState(models.TextChoices):
    """стейты исполнения для проектов и тасков"""

    EXECUTION = 'EXE', 'Создан'
    INWORK = 'IWO', 'В работе'
    FINISHED = 'FIN', 'Закончен'
    FROZEN = 'FRO', 'Заморожен'



class CommonAbstractModel(models.Model):
    """
        Абстрактная модель для хранения общих данных
        Абстрактная модель не создает таблицу в базе данных при запуске миграций, но зато от неё можно наследоваться и расширять наши модели.
    """

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    state = models.CharField(max_length=3, choices=ChoicesState.choices, default=ChoicesState.EXECUTION, verbose_name='Состояние исполнения')
    d_start = models.DateTimeField(blank=True, null=True, verbose_name="Дата Начала")
    d_end = models.DateTimeField(blank=True, null=True, verbose_name="Дата Окончания")
    completion_date = models.DateTimeField(blank=True, null=True, verbose_name='Сроки исполнения')


    def update(self, *args, **kwargs):
        """для прослеживания времени выполнения задачи"""
        if self.state=='EXE':
            self.d_end, self.d_start = None, None
        elif self.state=='IWO':
            if self.d_start==None:
                self.d_start, self.d_end = datetime.now(), None
            elif self.d_start!=None:
                self.d_end = None
        elif self.state=='FIN':
            self.d_end = datetime.now()
            if self.d_start==None:
                self.d_start = datetime.now()
        elif self.state=='FRO':
            if self.d_end != None:
                self.d_end = None
            if self.d_start==None:
                self.d_start = datetime.now()
        super().update(*args, **kwargs)

    def save(self, *args, **kwargs):
        """для прослеживания времени выполнения задачи"""
        if self.state=='EXE':
            self.d_end, self.d_start = None, None
        elif self.state=='IWO':
            if self.d_start==None:
                self.d_start, self.d_end = datetime.now(), None
            elif self.d_start!=None:
                self.d_end = None
        elif self.state=='FIN':
            self.d_end = datetime.now()
            if self.d_start==None:
                self.d_start = datetime.now()
        elif self.state=='FRO':
            if self.d_end != None:
                self.d_end = None
            if self.d_start==None:
                self.d_start = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def get_state(self):
        return ChoicesState(self.state).label

    def __str__(self):
        return self.name



class Project(CommonAbstractModel):
    """модель проектов"""

    #name, description, time_create, completion_date, state

    user = models.ManyToManyField(User, blank=True, verbose_name = 'Участник', related_name='user')

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse("shedm:project_detail", kwargs={"pk": self.pk})

    def project_period(self):
        """вычисляет оставшиеся дни до завершения проекта"""
        if self.completion_date:    #Если есть дата окончания проекта, то будем отражать время по дате окончания
            comp_date = time_zon(self.completion_date)
            days = (comp_date.date()-datetime.now().date()).days
            if days==0:
                return f"Проект нужно закончить сегодня"
            elif days>0:
                return f"Проект нужно закончить через {days} {word_form('день', days)}"
            elif days<0:
                return f"Проект просрочен на {abs(days)} {word_form('день', abs(days))}"
        elif not self.completion_date and self.d_start:    #если нет даты окончания но есть дата начала, ориентировка будет по дате начала
            if not self.d_end:    #Если пока не установлена дата окончания
                d_start = time_zon(self.d_start)
                days = (datetime.now().date()-d_start.date()).days
                return f"Проект в работе {days+1} {word_form('день', days+1)}"
            elif self.d_start and self.d_end:
                d_start = time_zon(self.d_start)
                d_end = time_zon(self.d_end)
                days = (d_end-d_start).days+1
                return f"Проект закончен за {days} {word_form('день', days)}"



class Task(CommonAbstractModel):
    """модель задач"""

    #name, description, time_create, completion_date, state

    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Создатель задачи')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Исполнитель задачи', related_name = 'executor')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект', related_name = 'project')
    priority = models.FloatField(null=True, blank=True, default=0, verbose_name='Приоритет')    #как установить максимальное значение


    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['time_create']


class Comment(models.Model):
    """Комменты к таске"""
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name = 'Кто написал комментарий')
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Задача')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Проект')
    text = models.TextField(blank=True, verbose_name='Текст комментария')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    comment = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE, verbose_name='Связанный комментарий',  related_name='related_comment')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['time_create']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)