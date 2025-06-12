from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("reg/", views.register_view, name="register"),
    path("welcome/", views.welcome_page, name="welcome_page"),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]