from django.db.models import F
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Category


class IndexView(View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by(F("number_on_main_page").asc(nulls_last=True))
        context = {"categories": categories}
        return render(request, template_name=self.template_name, context=context)


class About(TemplateView):
    template_name = "core/about.html"


class Contact(TemplateView):
    template_name = "core/contact.html"
