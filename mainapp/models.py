from django.db import models


class Person(models.Model):

    full_name = models.CharField('ФИО', max_length=128)
    score = models.FloatField('Рейтинг')
    qty_subscribers = models.PositiveIntegerField('Количество подписчиков')
    subscriptions = models.PositiveIntegerField('Количество подписок')
    qty_posts = models.PositiveIntegerField('Количество постов')
    avg_amount_likes_on_all_posts = models.FloatField('Среднее количество лайков на всех постах')
    avg_amount_likes_on_last_20_posts = models.FloatField('Среднее количество лайков на последних 20 постах')

    def __str__(self):
        return self.full_name
