"""tasks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskList.as_view(), name='tasks_list'),
    path('new/', views.TaskCreate.as_view(), name='tasks_new'),
    path('task/<int:pk>', views.TaskDetails.as_view(), name='tasks_view'),
    path('edit/<int:pk>', views.TaskUpdate.as_view(), name='tasks_edit'),
    path('delete/<int:pk>', views.TaskDelete.as_view(), name='tasks_delete'),
]
