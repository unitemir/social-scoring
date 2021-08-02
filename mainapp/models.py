from django.db import models


class InstagramUser(models.Model):

    qty_subscribers = models.PositiveIntegerField('Количество подписчиков')
    qty_posts = models.PositiveIntegerField('Количество постов')
    avg_amount_likes_on_all_posts = models.FloatField(
        'Среднее количество лайков на всех постах'
    )
    avg_amount_likes_on_last_20_posts = models.FloatField(
        'Среднее количество лайков на последних 20 постах'
    )
    subscriptions = models.PositiveIntegerField('Количество подписок')