from ..models import Person

from ..tasks import *


def test_successful_parce_vk(db):
    create_new_vk_person('id165028790')
    person_vk = Person.objects.all().reverse()[0]
    assert person_vk.social_network == 'VK'