from django.urls import path

from . import views
app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", views.About.as_view(), name="about"),
    path("contact", views.Contact.as_view(), name="contact"),
    path("api/subscribe", views.SubscribeView.as_view(), name="subscribe"),
]
