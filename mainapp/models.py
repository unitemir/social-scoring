from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class PersonStats(models.Model):

    qty_subscribers = models.PositiveIntegerField('Количество подписчиков', null=True, blank=True)
    subscriptions = models.PositiveIntegerField('Количество подписок', null=True, blank=True)
    qty_posts = models.PositiveIntegerField('Количество постов', null=True, blank=True)
    avg_amount_likes_on_all_posts = models.FloatField('Среднее количество лайков на всех постах', null=True, blank=True)
    avg_amount_likes_on_last_20_posts = models.FloatField('Среднее количество лайков на последних 20 постах', null=True, blank=True)


class Person(models.Model):

    full_name = models.CharField('ФИО', max_length=128)
    score = models.FloatField('Рейтинг', null=True, blank=True)
    stats = models.ForeignKey('PersonStats', on_delete=models.CASCADE, null=True, blank=True)
    friends = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')

    def __str__(self):
        return self.full_name

    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship

    def get_relationships(self, status):
        return self.friends.filter(
            to_people__status=status,
            to_people__from_person=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class Relationship(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_people', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)


class InstagramAccount(models.Model):

    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class FacebookAccount(models.Model):

    cookie_json = models.TextField()


class Proxy(models.Model):

    ip = models.CharField(max_length=255)