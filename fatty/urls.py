"""fatty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, static
from django.conf import settings
from dashboard.views import aqi
from excise import views

# from django.contrib import admin

urlpatterns = [
                  url(r'^$', aqi, name='index'),
                  url(r'^excise-a/', views.a),
                  url(r'^excise-b/', views.b),
                  url(r'^excise-c/', views.c),
                  url(r'^dashboard/', include('dashboard.urls')),
                  url(r'^api/aqi/', include('aqi.urls')),
                  url(r'^api/stock/', include('stock.urls')),
              ] + static.static(settings.STATIC_URL,
                                document_root=settings.STATIC_ROOT)
