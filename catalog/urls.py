from django.urls import path

from . import views
app_name = "catalog"
urlpatterns = [
    path("<int:id>", views.CategoryView.as_view(), name="category"),
    path("catalog_item/<int:id>", views.CatalogItemView.as_view(), name="catalog_item")
    # path("about", views.About.as_view(), name="about"),
    # path("contact", views.Contact.as_view(), name="contact"),
]
