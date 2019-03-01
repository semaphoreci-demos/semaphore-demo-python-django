"""
    Unit Test file for views
"""
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task


class TaskListViewTest(TestCase):
    """
    Test View class
    """
    @classmethod
    def setUpTestData(cls):
        """
        :return: None
        """
        number_of_tasks = 20
        for task_id in range(number_of_tasks):
            Task.objects.create(
                task_title='Task { task_id }',
                task_description='This is task number { task_id }. Lorem ipsum dolor sit amet, consectetur adipiscing',
            )

    def test_view_url(self):
        """
        :return: None
        """
        response = self.client.get('task/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        """
        :return: None
        """
        response = self.client.get(reverse('tasks:tasks_list'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        """
        :return: None
        """
        response = self.client.get(reverse('tasks:tasks_list'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
