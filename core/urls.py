from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", views.About.as_view(), name="about")
]
