"""
Task app: Views file
"""
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from tasks.models import Task


class TaskList(ListView):
    """
    Task list Generic List View
    """
    model = Task
    ordering = ['-task_created']

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context.update({'nlink': 'list'})
        return context


class TaskCreate(CreateView):
    """
    Task list Generic Create View
    """
    model = Task
    fields = ['task_title', 'task_description']
    success_url = reverse_lazy('tasks:tasks_list')

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context.update({'nlink': 'new'})
        return context


class TaskDetails(DetailView):
    """
    Task list Detail View
    """
    model = Task
    fields = ['task_title', 'task_description', 'task_created', 'task_updated']


class TaskUpdate(UpdateView):
    """
    Task list Update View
    """
    model = Task
    fields = ['task_title', 'task_description']
    success_url = reverse_lazy('tasks:tasks_list')

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context.update({'nlink': 'update'})
        return context


class TaskDelete(DeleteView):
    """
    Task list Delete View
    """
    model = Task
    success_url = reverse_lazy('tasks:tasks_list')


class Custom404(TemplateView):
    """
    Task list Custom 404 View
    """
    template_name = 'tasks/404.html'


class Custom500(TemplateView):
    """
    Task list Custom 500 View
    """
    template_name = 'tasks/500.html'
