from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Person(MPTTModel):

    full_name = models.CharField('ФИО', max_length=128)
    score = models.FloatField('Рейтинг', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    qty_subscribers = models.PositiveIntegerField('Количество подписчиков', null=True, blank=True)
    subscriptions = models.PositiveIntegerField('Количество подписок', null=True, blank=True)
    qty_posts = models.PositiveIntegerField('Количество постов', null=True, blank=True)
    avg_amount_likes_on_all_posts = models.FloatField('Среднее количество лайков на всех постах', null=True, blank=True)
    avg_amount_likes_on_last_20_posts = models.FloatField('Среднее количество лайков на последних 20 постах', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['full_name']

    def __str__(self):
        return self.full_name
