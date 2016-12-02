from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListEmployee.as_view(), name='employee_list')
]
