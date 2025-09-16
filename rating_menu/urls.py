from django.urls import path
from . import views


urlpatterns = [
    path("films/", views.index, name="rating_menu"),
    path("<slug:slug>", views.index, name="rating_menu"),
    # path("", views)
]

# from .views_class import IndexView

# urlpatterns = [
#     path('rating_menu/<slug:slug>/', IndexView.as_view(), name='rating_menu'),
    
# ]