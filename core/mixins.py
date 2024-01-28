from django.db.models import F
from django.views import View

from catalog.models import Category


class TopMenuMixin(View):
    def __init__(self):
        super().__init__()
        self.categories = Category.objects.all().order_by(F("number_on_main_page").asc(nulls_last=True))
        self.context = {}

    def dispatch(self, request, *args, **kwargs):
        cart_item_count = request.COOKIES.get('cart_item_count')
        cart_item_count = cart_item_count if cart_item_count else 0

        self.context = {
            'categories': self.categories,
            'cart_item_count': cart_item_count,
        }
        return super().dispatch(request, *args, **kwargs)
