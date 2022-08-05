from django.contrib import admin
from django.urls import path

from files import views


urlpatterns = [
    path('', views.index),
    path('upload', views.upload_file, name="upload_file"),
    path('admin/', admin.site.urls),
]
