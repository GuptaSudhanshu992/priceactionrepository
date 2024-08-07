from django.contrib import admin
from django.urls import include, path
from .views import BlogView, DetailArticleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('<slug:post_url>/', DetailArticleView.as_view(), name='blogpost'),
]