"""
    Unit test file for models
"""
from django.test import TestCase

from tasks.models import Task


class TaskModelTest(TestCase):
    """
    Test Model class
    """
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        # Setting up objects which can be use for all test methods
        Task.objects.create(task_title='Development', task_description='This task includes all the development '
                                                                       'related activities for this project')

    def test_task_title_label(self):
        """
        :return: None
        """
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('task_title').verbose_name
        self.assertEqual(field_label, 'Task Title')

    def test_task_description_label(self):
        """
        :return: None
        """
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('task_description').verbose_name
        self.assertEqual(field_label, 'Task Description')

    def test_get_absolute_url(self):
        """
        :return: None
        """
        task = Task.objects.get(id=1)
        self.assertEqual(task.get_absolute_url(), '/edit/1')
