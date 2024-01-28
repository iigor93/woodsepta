from django.urls import path

from . import views
app_name = "catalog"
urlpatterns = [
    path("<int:id>", views.CategoryView.as_view(), name="category"),
    path("catalog_item/<int:id>", views.CatalogItemView.as_view(), name="catalog_item"),
    path("cart", views.CartView.as_view(), name="cart"),
    path("order", views.OrderView.as_view(), name="order"),
    path("clear_cart", views.ClearCartView.as_view(), name="clear_cart"),
    path("search", views.SearchView.as_view(), name="search"),
]
