from django.urls import include, path, re_path
from django.contrib import admin

from tasks import views as task
from lists.views import home_page


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', home_page, name='home'),
    re_path(r'^lists/', include('lists.urls')),
    #path('task/', include('tasks.urls'))
]

#handler404 = task.Custom404.as_view()
#handler500 = task.Custom500.as_view()
