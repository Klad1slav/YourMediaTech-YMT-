from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="rating_menu")
]
