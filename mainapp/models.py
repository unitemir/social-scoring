from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Person(MPTTModel):

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

    social_network = models.CharField(
        'Соцсеть',
        max_length=128,
        choices=SOCIAL_NETWORKS_CHOICES,
        default=DEFAULT
    )
    username = models.CharField('Имя пользователя', max_length=128)
    score = models.FloatField('Рейтинг')
    qty_subscribers = models.PositiveIntegerField('Количество подписчиков', blank=True, null=True)
    qty_posts = models.PositiveIntegerField('Количество постов', blank=True, null=True)
    avg_amount_likes_on_all_posts = models.FloatField(
        'Среднее количество лайков на всех постах',
        blank=True,
        null=True
    )
    avg_amount_likes_on_last_20_posts = models.FloatField(
        'Среднее количество лайков на последних 20 постах',
        blank=True,
        null=True
    )
    subscriptions = models.PositiveIntegerField('Количество подписок', blank=True, null=True)
    parent = TreeForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    def __str__(self):
        return self.username