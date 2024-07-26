from django.contrib import admin
from django.urls import include, path
from .views import BlogView, DetailArticleView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('<int:pk>', DetailArticleView.as_view(), name='blog_post'),
]