import datetime

from django.db.models import F
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from catalog.models import Category, CategoryItem
from core.mixins import TopMenuMixin


class CategoryView(TopMenuMixin, ListView):
    model = CategoryItem
    template_name = "catalog/category.html"
    paginate_by = 16

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        items = qs.filter(category_id=self.kwargs['id'])
        return items

    def get_context_data(self, **kwargs):
        self.context.update(super().get_context_data(**kwargs))
        category = Category.objects.filter(id=self.kwargs['id']).first()
        self.context.update({"category": category})
        return self.context


class CatalogItemView(TopMenuMixin, View):
    template_name = "catalog/catalog_item.html"

    def get(self, request, *args, **kwargs):

        main_attribute_id = request.GET.get("attribute")
        catalog_item_id = kwargs["id"]
        catalog_item = CategoryItem.objects.get(id=catalog_item_id)

        if main_attribute_id:
            current_attribute = catalog_item.main_attribute.filter(id=main_attribute_id).get()
        else:
            current_attribute = catalog_item.main_attribute.all().first()
        sliders = catalog_item.slider.all()

        show_cart_add_button = True
        items = request.COOKIES
        for item in items.keys():
            if item.startswith("catalog_item"):
                attribute = item.split("&")[1:]
                if attribute[0] == str(catalog_item_id) and attribute[1] == str(current_attribute.id):
                    show_cart_add_button = False

        self.context.update({
                        "catalog_item": catalog_item,
                        "sliders": sliders,
                        "current_attribute": current_attribute,
                        "current_price": catalog_item.price + current_attribute.additional_price,
                        "show_cart_add_button": show_cart_add_button,
                        })
        return render(request, template_name=self.template_name, context=self.context)


class CartView(TopMenuMixin, View):
    template_name = "catalog/cart.html"

    def get(self, request, *args, **kwargs):
        cart_is_empty = False
        items = request.COOKIES
        for item in items.keys():
            if item.startswith("catalog_item"):
                pass

        self.context.update({"cart_is_empty": cart_is_empty})
        return render(request, template_name=self.template_name, context=self.context)


class OrderView(TopMenuMixin, View):
    template_name = "catalog/order.html"

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.COOKIES)
        current_date = datetime.datetime.now()
        items = request.COOKIES
        cart_items = []
        for item in items.keys():
            if item.startswith("catalog_item"):
                cart_items.append(item)

        # TODO распарсить товар и сохранить в модель
        # TODO отправить письмо о новом заказе

        self.context.update(
            {"order_number": 345,
             "order_date": current_date,
             "cart_item_count": 0,
             }
        )
        response = render(request, template_name=self.template_name, context=self.context)

        for i in cart_items:
            response.delete_cookie(i)
        response.delete_cookie("cart_item_count")
        return response
