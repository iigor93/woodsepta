from django.db import models


class Subscriber(models.Model):

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")
    email = models.CharField(max_length=100, verbose_name="email")
