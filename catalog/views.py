from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from catalog.models import Category, CategoryItem


# Create your views here.

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")


class CatalogItemView(View):
    template_name = "catalog/catalog_item.html"

    def get(self, request, *args, **kwargs):
        main_attribute_id = request.GET.get("attribute")
        categories = Category.objects.all().order_by(F("number_on_main_page").asc(nulls_last=True))
        catalog_item_id = kwargs["id"]
        catalog_item = CategoryItem.objects.get(id=catalog_item_id)

        if main_attribute_id:
            current_attribute = catalog_item.main_attribute.filter(id=main_attribute_id).get()
        else:
            current_attribute = catalog_item.main_attribute.all().first()
        sliders = catalog_item.slider.all()
        context = {"categories": categories,
                   "catalog_item": catalog_item,
                   "sliders": sliders,
                   "current_attribute": current_attribute,
                   "current_price": catalog_item.price + current_attribute.additional_price
                   }
        return render(request, template_name=self.template_name, context=context)
