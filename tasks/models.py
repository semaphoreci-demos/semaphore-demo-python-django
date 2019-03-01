"""
    Task model
"""
from django.db import models
from django.urls import reverse


class Task(models.Model):
    """
    Stores a single Task entry
    """
    task_title = models.CharField(max_length=50, verbose_name='Task Title')
    task_description = models.TextField(max_length=200, verbose_name='Task Description')
    task_created = models.DateTimeField(auto_now_add=True)
    task_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        :return: string to represent Task model
        """
        return self.task_title

    def get_absolute_url(self):
        """
        :return: returns the absolute url for task model
        """
        return reverse('tasks:tasks_edit', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
