from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('like', views.like, name='like'),
    path('auth', views.auth, name='auth'),
    path('callback', views.callback, name="auth_return"),
]