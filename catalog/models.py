from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=50, verbose_name='Название категории', null=False)
    description = models.TextField(verbose_name='Описание категории', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name='Заголовок категории', null=True, blank=True)
    image = models.ImageField(upload_to='images/category/', verbose_name='Фото категории')
    number_on_main_page = models.PositiveSmallIntegerField(verbose_name="Номер на первой странице", null=True, blank=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    name = models.CharField(max_length=50, verbose_name='Название фото')
    image = models.ImageField(upload_to='images/all/', verbose_name='Фото')

    def __str__(self):
        return self.name


class MainAttribute(models.Model):
    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    name = models.CharField(max_length=50, verbose_name='Название атрибута', null=False)
    title = models.CharField(max_length=50, verbose_name='Заголовок атрибута', null=False)
    additional_price = models.FloatField(verbose_name="Добавленная цена", default=0.0)
    thumbnail = models.ImageField(verbose_name="Логотип атрибута (мини)", upload_to='images/attribute/')
    item_photos = models.ManyToManyField(Photo, verbose_name="Фото товара с атрибутом")
    vendor_code = models.CharField(max_length=50, verbose_name='Артикул товара с атрибутом', null=False)
    delivery_days = models.IntegerField(verbose_name="Производство дней", null=True, blank=True)

    def __str__(self):
        return self.name


class SliderAttribute(models.Model):
    class Meta:
        verbose_name = "Атрибут слайдер"
        verbose_name_plural = "Атрибуты слайдер"
    name = models.CharField(max_length=50, verbose_name='Название атрибута слайдера', null=False)
    title = models.CharField(max_length=50, verbose_name='Заголовок атрибута слайдера', null=False)
    description = models.TextField(verbose_name='Описание слайдера')
    start_value = models.PositiveIntegerField(default=0, verbose_name="Начальное значение слайдера", null=False)
    stop_value = models.PositiveIntegerField(default=100, verbose_name="Конечное значение слайдера", null=False)

    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("id",)

    name = models.CharField(max_length=50, verbose_name='Название товара', null=False)
    description = models.TextField(verbose_name='Описание товара')
    price = models.FloatField(verbose_name="Цена", default=0.0)
    vendor_code = models.CharField(max_length=50, verbose_name='Артикул товара', null=False)
    main_attribute = models.ManyToManyField(MainAttribute, verbose_name="Основной атрибут", related_name='category_items', blank=True)
    slider = models.ManyToManyField(SliderAttribute, verbose_name="Слайдер атрибут", related_name='category_items', blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT)
    item_photos = models.ManyToManyField(Photo, verbose_name="Фото товара", blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата время заказа")
    description = models.TextField(verbose_name="Текст заказа")
    contact = models.TextField(verbose_name="Контакты")
    comment = models.TextField(verbose_name="Комментарий к заказу", null=True, blank=True)
