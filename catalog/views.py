import datetime

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from catalog.models import Category, CategoryItem, MainAttribute, SliderAttribute, Order
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
        cart_is_empty = True
        items = request.COOKIES
        cart_items = []
        total_sum = 0
        for item in items.keys():
            if item.startswith("catalog_item"):
                attributes = item.split("&")[1:]
                item_text = "<br> - "
                for index, attribute_item in enumerate(attributes):
                    if index == 0:
                        catalog_item = CategoryItem.objects.filter(id=attribute_item).first()
                        item_text += f"{catalog_item.name}<br>"
                    elif index == 1:
                        main_attribute = MainAttribute.objects.filter(id=attribute_item).first()
                        item_text += f"Главный атрибут: {main_attribute.name}.<br>"
                    elif attribute_item.startswith("sl"):
                        slider_list = attribute_item.split("_")
                        slider_attribute = SliderAttribute.objects.filter(id=slider_list[1]).first()
                        item_text += f"Дополнительные параметры: {slider_attribute.name}, Значение {slider_list[2]}.<br>"

                total_sum += catalog_item.price + main_attribute.additional_price
                cart_items.append((catalog_item, main_attribute, item_text, catalog_item.price + main_attribute.additional_price))

        if len(cart_items) > 0:
            cart_is_empty = False

        self.context.update({"cart_is_empty": cart_is_empty, "cart_items": cart_items, "total_sum": total_sum})
        return render(request, template_name=self.template_name, context=self.context)


class OrderView(TopMenuMixin, View):
    template_name = "catalog/order.html"

    def post(self, request, *args, **kwargs):
        items = request.COOKIES
        cart_items = []
        cookie_items = []
        for item in items.keys():
            if item.startswith("catalog_item"):
                cookie_items.append(item)
                attributes = item.split("&")[1:]
                item_text = "\n - "
                for index, attribute_item in enumerate(attributes):
                    if index == 0:
                        catalog_item = CategoryItem.objects.filter(id=attribute_item).first()
                        item_text += f"Товар № {catalog_item.id} {catalog_item.name}, цена {catalog_item.price}.\n"
                    elif index == 1:
                        main_attribute = MainAttribute.objects.filter(id=attribute_item).first()
                        item_text += f"Главный атрибут {main_attribute.id} {main_attribute.name}, цена {main_attribute.additional_price}.\n"
                    elif attribute_item.startswith("sl"):
                        slider_list = attribute_item.split("_")
                        slider_attribute = SliderAttribute.objects.filter(id=slider_list[1]).first()
                        item_text += f"Доп атрибут {slider_attribute.id} {slider_attribute.name}, Значение {slider_list[2]}.\n"

                cart_items.append(item_text)

        order = Order.objects.create(contact=request.POST.get("phone_email"),
                                     comment=request.POST.get("comment"),
                                     description="; ".join(cart_items))

        self.context.update(
            {"order_number": order.id,
             "order_date": order.date_created,
             "cart_item_count": 0,
             }
        )
        response = render(request, template_name=self.template_name, context=self.context)

        for i in cookie_items:
            response.delete_cookie(i)
        response.delete_cookie("cart_item_count")
        return response


class ClearCartView(View):

    def get(self, request, *args, **kwargs):

        items = request.COOKIES
        cookie_items = []
        for item in items.keys():
            if item.startswith("catalog_item"):
                cookie_items.append(item)

        response = HttpResponseRedirect(reverse("core:index"))

        for i in cookie_items:
            response.delete_cookie(i)
        response.delete_cookie("cart_item_count")
        return response
