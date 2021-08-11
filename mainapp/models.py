from django.db import models


class Person(models.Model):

    DEFAULT = 'none'
    FACEBOOK = 'Facebook'
    INSTAGRAM = 'Instagram'
    VK = 'VK'
    SOCIAL_NETWORKS_CHOICES = [
        (DEFAULT, 'Значение по умолчанию'),
        (FACEBOOK, 'Facebook'),
        (INSTAGRAM, 'Instagram'),
        (VK, 'vk'),
    ]

    social_network = models.CharField('Соцсеть', max_length=128, choices=SOCIAL_NETWORKS_CHOICES, default=DEFAULT)
    qty_subscribers = models.PositiveIntegerField('Количество подписчиков')
    qty_posts = models.PositiveIntegerField('Количество постов')
    avg_amount_likes_on_all_posts = models.FloatField(
        'Среднее количество лайков на всех постах'
    )
    avg_amount_likes_on_last_20_posts = models.FloatField(
        'Среднее количество лайков на последних 20 постах'
    )
    subscriptions = models.PositiveIntegerField('Количество подписок')