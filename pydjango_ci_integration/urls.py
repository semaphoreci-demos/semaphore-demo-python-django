from django.urls import include, path
from django.contrib import admin

from tasks import views as task
from lists import views as list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', list.home_page, name='home'),
    path('task/', include('tasks.urls'))
]

handler404 = task.Custom404.as_view()
handler500 = task.Custom500.as_view()
