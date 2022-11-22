from django.urls import include, path
from django.contrib import admin

from tasks import views
from lists import views as list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', list.home_page, name='home'),
    path('', include('tasks.urls'))
]

handler404 = views.Custom404.as_view()
handler500 = views.Custom500.as_view()
