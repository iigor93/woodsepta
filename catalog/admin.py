from django.contrib import admin

from catalog.models import Category, Photo, MainAttribute, SliderAttribute, CategoryItem

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(MainAttribute)
admin.site.register(SliderAttribute)
admin.site.register(CategoryItem)
