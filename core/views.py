from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Category, CategoryItem
from core.mixins import TopMenuMixin
from core.models import Subscriber


class IndexView(TopMenuMixin, View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):

        fist_page_categories = self.categories.filter(number_on_main_page__isnull=False)
        items_list = []
        for category in fist_page_categories:
            items = CategoryItem.objects.filter(category=category)[:5]
            items_list.extend(list(items))

        self.context.update({"items_list": items_list})
        return render(request, template_name=self.template_name, context=self.context)


class About(TopMenuMixin, TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        return self.context


class Contact(TopMenuMixin, TemplateView):
    template_name = "core/contact.html"

    def get_context_data(self, **kwargs):
        return self.context


class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if email:
            Subscriber.objects.create(email=email)

        return HttpResponseRedirect(reverse("core:index"))
