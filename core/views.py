from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class IndexView(View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class About(TemplateView):
    template_name = "core/about.html"
