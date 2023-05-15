#!/usr/bin/env python
# -- coding: utf-8 --
"""

"""
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required    #декоратор доступа только регистрированым пользователям
from django.views.generic import ListView, DetailView
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from shed.forms import (RegisterUserForm, LoginUserForm, ProjectCreateForm,
                        CommentForm, TaskCreateForm, TaskUpdateStateForm)
from shed.models import Project, Task, Comment, User

from database import api as db_api
from database.api import RecordClass


def home(request):
    return render(request,"shed/home/home.html")


class ProjectDetail(LoginRequiredMixin, DetailView):
    """вывод информации о проекте"""
    template_name = 'shed/project/proj_info.html'
    model = Project
    context_object_name: str = 'project'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_object(self):
        pk = self.kwargs.get('pk')
        return db_api.get_project(pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        project: RecordClass = context['object'][0]
        context["project"] = project
        context['state'] = project.get_state()
        user_list = [i.username for i in context['object'][:] if i.username]
        print(user_list)
        context['user_list'] = user_list
        if project.d_start:
            context['start'] = project.d_start
        if project.d_end:
            context['end'] = project.d_end
        if project.completion_date:
            context['completion_date'] = project.completion_date.date()
        if project.d_end and project.d_start:
            period = project.d_end-project.d_start
            context['period']=period.days+1   #За сколько дней был закончен проект
        elif project.d_start and (project.d_end==None):
            counting = datetime.now().date()-project.d_start.date()
            context['counting'] = counting.days+1    #сколько продолжается
        return context


class TaskInfo(LoginRequiredMixin, DetailView):
    """Вывод информации о задаче"""
    template_name = 'shed/task/task_info.html'
    model = Task
    context_object_name: str = 'task'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_object(self):
        pk = self.kwargs.get('pk')
        return db_api.task_info(pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        task = context['object'][0]
        context['task'] = task
        comment_list = context['object'][:]
        comment = []
        bount_comment = []
        for i in comment_list:
            if i.__dict__['connect_comment']!=None and i.__dict__['comment_id']:
                bount_comment.append(i)
            elif i.__dict__['connect_comment']==None and i.__dict__['comment_id']:
                comment.append(i)
        context['comment'] = comment
        context['bount_comment'] = bount_comment
        return context

        # {'proj_id': 13, 'proj_name': 'Проект 1', 'username': 'shed_admin3', 'id': 130, 'name': 'Создана со сроком', 'description': None,
        # 'time_create': datetime.datetime(2022, 11, 9, 15, 59, 13, 470716), 'completion_date': datetime.datetime(2022, 11, 9, 16, 10),
        # 'state': 'IWO', 'priority': 0.0, 'project_id': 13, 'd_end': None, 'd_start': datetime.datetime(2022, 11, 10, 10, 16, 4, 289449),
        # 'creator_id': 1, 'executor_id': 12, 'connect_comment': None, 'autor_comment_id': 13, 'create_comment': datetime.datetime(2022, 11, 10, 11, 12, 49, 287977),
        # 'text_comment': 'второй комментарий к задаче со сроком', 'comment_id': 107, 'autor_comment': 'shed_admin4'}


class ProjectsView(LoginRequiredMixin, ListView):
    """Все проекты"""
    model = Project  # ссылается на модель связанный с отображаемым списком
    template_name = 'shed/project/all_project.html'  # явно указали путь
    context_object_name = 'projects'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован


class UserList(LoginRequiredMixin, ListView):
    """список юзеров для удаления суперпользователем"""
    model = User
    template_name: str = 'shed/accounts/user_list.html'
    context_object_name = 'users'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован


class CommentView(LoginRequiredMixin, ListView):
    """комментарии"""
    model = Comment
    ordering = '-time_create'
    template_name = 'shed/comment/proj_all_comment.html'
    context_object_name = 'comment'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return db_api.get_comment(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = context['object_list'][:]
        context['proj_id'] = self.kwargs['pk']
        commet = []
        bount_comment = []
        if len(context['object_list'])>0:
            proj = context['object_list'][0]
            context['proj'] = proj.proj_name
            for i in comment_list:
                if i.__dict__['comment_id']!=None:
                    bount_comment.append(i)
                elif i.__dict__['comment_id']==None:
                    commet.append(i)
            context['comment'] = commet
            context['bount_comment'] = bount_comment
        return context


class RegisterUser(CreateView):
    """регистрация пользователя"""

    form_class = RegisterUserForm
    template_name = 'shed/accounts/register.html'
    success_url = reverse_lazy('shedm:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """авторизация пользователя после регистрации"""
        user = form.save()
        login(self.request, user)
        return redirect('shedm:home')


class LoginUser(LoginView):
    """ пользователя"""
    form_class = LoginUserForm
    template_name = 'shed/accounts/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        """ перенаправление после успешного входа """
        return reverse_lazy('shedm:home')


@login_required
def logout_user(request):
    """ разлогинивание пользователя """
    logout(request)
    return redirect('shedm:home')


class AddProject(LoginRequiredMixin, CreateView):
    """Добавление проекта"""
    form_class = ProjectCreateForm
    template_name = 'shed/project/add_update.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """ сохранение """
        form.save()
        return redirect('shedm:projects')


class AddTaskComment(LoginRequiredMixin, CreateView):
    """добавление комментария к задаче"""
    form_class = CommentForm
    template_name = 'shed/task/task_info.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)    #данный из самой формы
            instance.user = self.request.user    #юзер который написал
            task = Task.objects.get(pk=self.kwargs.get('pk2', None))    #проект комментария
            instance.task = task
            comment_pk = self.kwargs.get('pk', None)   #проверка есть ли связанный комментарий
            if comment_pk:
                comment = Comment.objects.get(pk=comment_pk)
                instance.comment = comment
            instance.save()
            return redirect('shedm:task_info', pk2=self.kwargs.get('pk3', None), pk=self.kwargs.get('pk2',None))


class AddComment(LoginRequiredMixin, CreateView):
    """Добавление комментария"""
    form_class = CommentForm
    template_name = 'shed/comment/proj_all_comment.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def post(self, request, *args, **kwargs):
        """Переопределение для корректного сохранения """    #TODO КОРРЕКТНОГО
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)    #данный из самой формы
            instance.user = self.request.user    #юзер который написал
            proj = Project.objects.get(pk=self.kwargs.get('pk', None))    #проект комментария
            instance.project = proj
            comment_pk = self.kwargs.get('pk2', None)   #проверка есть ли связанный комментарий
            if comment_pk:
                comment = Comment.objects.get(pk=comment_pk)
                instance.comment = comment
            instance.save()
            return redirect('shedm:comment_proj', pk=self.kwargs.get('pk', None))


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    """Изменение проекта"""
    form_class = ProjectCreateForm
    model = Project
    context_object_name: str = 'project'
    template_name = 'shed/project/add_update.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован
    success_url = reverse_lazy('shedm:projects')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete'] = 'Удалить'
        return context


class UserUpdate(LoginRequiredMixin, UpdateView):
    """изменение юзера"""
    form_class = RegisterUserForm
    model = User
    context_object_name: str = 'user'
    template_name = 'shed/accounts/update_user.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован
    success_url = reverse_lazy('shedm:projects')


class TaskUpdateState(LoginRequiredMixin, UpdateView):
    """изменение статуса задачи"""
    form_class = TaskUpdateStateForm
    model = Task
    context_object_name: str = 'task'
    template_name = 'shed/task/update_state.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован
    success_url = reverse_lazy('shedm:projects')

    def get_context_data(self, *args, **kwargs):
        # context['pk2'] = self.kwargs.get('pk2')
        # context['pk'] = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)

    def form_valid(self, form):
        """ сохранение """
        form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class TaskProject(LoginRequiredMixin, ListView):
    """Все задачи проекта"""
    model = Task
    template_name = 'shed/task/proj_tasks.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy("shedm:login")

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        pk2 = self.kwargs.get('pk2', None)
        return db_api.all_project_task(pk, pk2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_list = context['object_list'][:]
        users_list = db_api.get_users(project_id=self.kwargs.get('pk'))
        context['users'] = users_list
        context['proj_name'] = users_list[0].__dict__['project_name']
        context['pk'] = self.kwargs.get('pk')
        context['inwork'] = [i for i in task_list if i.state=='IWO']
        context['execution'] = [i for i in task_list if i.state=='EXE']
        context['finished'] = [i for i in task_list if i.state=='FIN']
        context['frozen'] = [i for i in task_list if i.state=='FRO']
        return context


class TaskUserList(LoginRequiredMixin, ListView):
    """Доска юзера"""
    model = Project
    template_name = 'shed/task/usertask.html'
    context_object_name = 'project'
    login_url = reverse_lazy("shedm:login")

    def get_queryset(self):
        project_id = self.kwargs.get('pk', None)
        user_id = self.request.user.id
        return db_api.get_tasks_board(project_id, int(user_id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proj_pk = self.kwargs.get('pk', None)
        context['proj_pk'] = proj_pk
        project_list = db_api.get_users_project(user_id=int(self.request.user.id))    #все проекты пользователя с колличеством зазач "в работе"
        context['project_list'] = project_list
        task_list = context['object_list'][:]    #наши таски для программы
        context['task_list'] = task_list
        context['inwork'] = [i for i in task_list if i.state=='IWO']
        context['execution'] = [i for i in task_list if i.state=='EXE']
        context['finished'] = [i for i in task_list if i.state=='FIN']
        context['frozen'] = [i for i in task_list if i.state=='FRO']
        return context

    #{'id': 14, 'name': 'Проект2', 'task_id': 102, 'task_name': 'зАДАЧА 1', 'task_time_create': datetime.datetime(2022, 11, 8, 12, 43, 59, 157245),
    # 'task_completion_date': datetime.datetime(2022, 11, 11, 15, 12), 'task_state': 'EXE', 'task_end': None, 'task_start': None, 'user_id': 1,
    # 'user_username': 'shed_admin', 'count': 2}



class AddTask(LoginRequiredMixin, CreateView):
    """Добавление задачи"""
    form_class = TaskCreateForm
    template_name = 'shed/task/add_task.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proj_pk'] = self.kwargs.get('pk')
        return context

    def get_form_kwargs(self):
        """передача в форму"""
        kwargs = super(AddTask, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        """ сохранение """
        if form.is_valid():
            instance = form.save(commit=False)    #данный из самой формы
            proj = Project.objects.get(pk=self.kwargs.get('pk', None))    #проект комментария
            instance.project = proj
            instance.creator = self.request.user
            instance.save()
            n = self.request.META.get('HTTP_REFERER')
            # http://127.0.0.1:4333/project/13/task/add/
            return redirect('shedm:all_task_project', pk=self.kwargs.get('pk', None))


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """Изменение задачи"""
    form_class = TaskCreateForm
    model = Task
    context_object_name: str = 'task'
    template_name = 'shed/task/update.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        context['pk2'] = self.kwargs.get('pk2')
        return context

    def get_form_kwargs(self):
        """передача в форму"""
        kwargs = super(TaskUpdate, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk2')
        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy('shedm:all_task_project', kwargs={'pk':self.kwargs.get('pk2', None)})


class TaskDelete(DeleteView):
    """Удаление задачи"""
    model = Task
    template_name = 'shed/task/task_info.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_success_url(self):
        return reverse_lazy('shedm:all_task_project', kwargs={'pk':self.kwargs.get('pk2', None)})


class TaskCommentDelete(DeleteView):
    """Удаление комментария задачи"""
    model = Comment
    template_name: str = 'shed/task/task_info.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_success_url(self):
        return reverse_lazy('shedm:task_info', kwargs={'pk2':self.kwargs.get('pk3', None),'pk':self.kwargs.get('pk2', None)})


class ProjectDelete(DeleteView):
    """Удаление проекта"""
    model = Project
    template_name = 'shed/project/add_update.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован
    success_url = reverse_lazy('shedm:projects')


class DeleteUser(DeleteView):
    """Удаление юзера"""
    model = User
    template_name = 'shed/accounts/user_list.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован
    success_url = reverse_lazy('shedm:user_list')


class CommentDelete(DeleteView):
    """Удаление комментария"""
    model = Comment
    template_name: str = 'shed/comment/proj_all_comment.html'
    login_url = reverse_lazy("shedm:login")  # куда перенаправить если пользователь не зарегистрирован

    def get_success_url(self):
        return reverse_lazy('shedm:comment_proj', kwargs={'pk':self.kwargs.get('pk2', None)})