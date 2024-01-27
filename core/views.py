from django.db.models import F
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Category
from core.mixins import TopMenuMixin


class IndexView(TopMenuMixin, View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context=self.context)


class About(TopMenuMixin, TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        return self.context


class Contact(TopMenuMixin, TemplateView):
    template_name = "core/contact.html"

    def get_context_data(self, **kwargs):
        return self.context
