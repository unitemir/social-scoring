from __future__ import absolute_import, unicode_literals
from conf.celery import app

from .models import Person
from .utils import *

from datetime import datetime

import json
import glob
import requests
import time
import re
import os
import random
from random import choice

from .grabber.instagram import Instagram
from .grabber.facebook import Facebook
from .grabber.instagram import InstagramStats

from .grabber.vk import VK


@app.task()
def create_instagram_person_three(instagram_username):
    inst = Instagram('elenaveselova3854', 'eKp7AMhoER')
    inst.auth()


    root_object = Person.objects.create(full_name=vk_id)
    friends = inst.get_friends_list_by_instagram_username(instagram_username)
    for root_friend in friends:
        try:
            root_friend_object = Person.objects.create(full_name=root_friend, parent=root_object)
            # for friend_lvl_2 in inst.get_friends_list_by_instagram_username(instagram_username):
            #     try:
            #         friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
            #     except:
            #         continue
        except:
            continue
    inst.close_browser()
    return True


@app.task()
def create_vk_person_three(vk_id):

    access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'

    def get_friends_list_by_vk_id(vk_id):
        get_vk_id_url = f'https://api.vk.com/method/users.get?user_ids={vk_id}&v=5.92&access_token={access_token}'
        get_vk_id = requests.get(get_vk_id_url).json()['response'][0]['id']
        get_user_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={get_vk_id}&fields=domain&v=5.92&access_token={access_token}'
        user_friends_list = requests.get(get_user_friends_list_url).json()['response']['items']
        return [friend['domain'] for friend in user_friends_list]

    root_object = Person.objects.create(full_name=vk_id)
    friends = get_friends_list_by_vk_id(vk_id)
    for root_friend in friends:
        try:
            root_friend_object = Person.objects.create(full_name=root_friend, parent=root_object)
            for friend_lvl_2 in get_friends_list_by_vk_id(root_friend):
                try:
                    friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
                except:
                    continue
        except:
            continue

    return True


# @app.task()
# def create_facebook_person_three(facebook_id):
#     fb = Facebook()
#     fb.auth()
#     friends = fb.get_friends_list_by_face_book_id(facebook_id)
#     print(friends)
#     print(len(friends))
#     return True