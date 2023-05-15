#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from django.urls import path
from shed.views import (home, logout_user, RegisterUser, LoginUser, AddProject,
                        ProjectsView, ProjectDetail, ProjectUpdate, ProjectDelete,
                        CommentView, AddComment, CommentDelete, TaskProject, AddTask,
                        TaskInfo, TaskDelete, TaskUpdateState, TaskCommentDelete,
                        AddTaskComment, TaskUpdate, TaskUserList, UserUpdate, UserList, DeleteUser)

app_name = 'shedm'

urlpatterns = [

    path('', home, name='home'),

    #__регистрация, вход и выход пользователя__
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user/<int:pk>/update/', UserUpdate.as_view(), name='update_user'),
    path('user/', UserList.as_view(), name='user_list'),    #список юзеров для удаления суперпользователем
    path('user/<int:pk>/delete', DeleteUser.as_view(), name='delete_user'),    #удаление юзера доступно только суперпользоватлю

    #добавдение проекта или задачи
    path('project/add/', AddProject.as_view(), name='add_project'),    #добавление проекта

    #проекты
    path('project/', ProjectsView.as_view(), name='projects'),    #все проекты
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),    #детальная информация о проекте
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),    #удаление проекта
    path('project/<int:pk>/update/', ProjectUpdate.as_view(), name='project_update'),    #изменение проекта


    #задачи
    path('project/<int:pk>/task/add/', AddTask.as_view(), name='add_task'),    #добавление задачи в проект
    path('project/<int:pk>/task/', TaskProject.as_view(), name='all_task_project'),    #все задачи проекта
    path('project/<int:pk>/task/user/<int:pk2>/', TaskProject.as_view(), name='filter_user'),   #фильтр задач по юзерам
    path('project/<int:pk2>/task/<int:pk>/', TaskInfo.as_view(), name='task_info'),    #инфо по задаче
    path('project/<int:pk2>/task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),    #удаление задачи
    path('project/<int:pk2>/task/<int:pk>/update_state/', TaskUpdateState.as_view(), name='task_state_update'),    #Изменение статуса задачи
    path('project/<int:pk2>/task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),    #Изменение задачи

    path('project/all_task/', TaskUserList.as_view(), name='all_user_task'),    #Все задачи пользователя
    path('project/<int:pk>/all_task/', TaskUserList.as_view(), name='all_user_project_task'),    #Все задачи пользователя по проекту
    path('project/<int:pk>/all_task/add/', AddTask.as_view(), name='add_all_task'),    #добавление задачи в проект

    #комментарии к проекту
    path('project/<int:pk>/comment/', CommentView.as_view(), name='comment_proj'),  #комментарии проекта
    path('project/<int:pk>/comment/add/', AddComment.as_view(), name='add_comment'),    #Добавление комментария
    path('project/<int:pk>/comment/add/<int:pk2>/', AddComment.as_view(), name='add_comment_bound'),    #Добавление комментария связанного
    path('project/<int:pk2>/comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),    #удаление комментария

    #комментарии к задаче
    path('project/<int:pk3>/comment/<int:pk2>/add/', AddTaskComment.as_view(), name='add_task_comment'),    #Добавление комментария
    path('project/<int:pk3>/comment/<int:pk2>/add/<int:pk>/', AddTaskComment.as_view(), name='add_task_comment_bound'),    #Добавление комментария связанного
    path('project/<int:pk3>/task/<int:pk2>/comment/<int:pk>/delete/', TaskCommentDelete.as_view(), name='task_comment_delete')    #удаление комментария из задачи
]