"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from news import views


# register viewsets, basename for correct link
router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset, basename='news')
router.register(r'articles', views.ArticleViewset, basename='articles')

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),               # inbuild endpoints with localisation
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('articles/', include('articles.urls')),
   path('', include('authorisation.urls')),
   path('', include('allauth.urls')),
   path('api/', include(router.urls)),                            # inclide links for REST API
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
