"""docker_manager URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from index import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^images_management/', views.images_management),
    url(r'^pull_images/', views.pull_images),
    url(r'^check_static_file/', views.status_check),
    url(r'^create_container/', views.create_container),
    url(r'^container_exec/', views.container_exec),
    url(r'^image_detail/', views.image_detail),
    url(r'^delete_image/', views.delete_image),
    url(r'^local_registry/', views.create_local_registry),
    url(r'^test_data/', views.test_data), # 测试数据

]
