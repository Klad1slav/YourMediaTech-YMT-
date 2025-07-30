from django.urls import path
from . import views


urlpatterns = [
    path("films/", views.index, name="rating_menu"),
    path("<slug:slug>", views.index, name="rating_menu"),
    # path("", views)
]
