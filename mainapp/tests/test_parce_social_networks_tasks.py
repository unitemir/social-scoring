from ..models import Person

from ..tasks import *


def test_successful_parce_instagram(db):
    create_new_instagram_user()
    inst_person = Person.objects.all().reverse()[0]
    assert inst_person.social_network == 'Instagram'


def test_successful_parce_vk(db):
    create_new_vk_person()
    vk_person = Person.objects.all().reverse()[0]
    assert vk_person.social_network == 'VK'


def test_successful_parce_facebook(db):
    get_facebook_friends_list()
    facebook_person = Person.objects.all().reverse()[0]
    assert facebook_person.social_network == 'Facebook'
