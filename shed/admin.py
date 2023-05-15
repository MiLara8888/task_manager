#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from django.contrib import admin
from shed.models import Task, Project, Comment
from django.db import models
from django.forms import CheckboxSelectMultiple


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # #'user', 'name', 'description', 'time_create', 'completion_date', 'state',

    list_display = ('name', 'state','d_start')        #отображение в списке
    fields = ('user', 'name', 'description', 'completion_date', 'state', 'd_start', 'd_end', 'time_create')
    list_display_links = ('name','state')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    readonly_fields = ('time_create',)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # 'user', 'name', 'description', 'time_create', 'completion_date', 'state', 'priority', 'project'
    list_display = ('name', 'creator', 'executor', 'state', 'project')        #отображение в списке
    fields = ('creator', 'executor', 'name', 'description', 'time_create', 'completion_date', 'state', 'priority', 'project', 'd_start', 'd_end')
    list_display_links = ('name', 'creator', 'executor')
    ordering = ('-time_create',)    #закоментить, чтобы база работала быстрее
    search_fields = ('creator', 'name' , 'executor')
    readonly_fields = ('time_create',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 'comment', 'text', 'task', 'user', 'time_create'
    fields = ('comment', 'text', 'task', 'user', 'time_create','project')
    list_display = ('task', 'project', 'user', 'time_create')
    list_display_links = ('task', )
    search_fields = ('user', )
    readonly_fields = ('time_create',)
    ordering = ('-time_create',)    #закоментить, чтобы база работала быстрее



admin.site.site_header = ('Админ-панель task менеджера')
admin.site.site_title = ('Админ-панель task менеджера')
admin.site.empty_value_display = '(None)'