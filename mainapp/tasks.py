from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .grabber.instagram import InstagramStats
from .models import Person
from .utils import *

import os
import re
import time
import requests
import json
import glob
import random

from datetime import datetime

from random import choice

from .grabber.instagram import Instagram
from .grabber.facebook import Facebook
from .grabber.instagram import InstagramStats
from .grabber.vk import VK


@app.task()
def get_instagram_friend_list_by_instagram_username(instagram_username):

    inst = Instagram('fevroniia8667', 'ZqmkM0Pp')
    inst.auth()

    try:
        root_object = Person.objects.get(full_name=instagram_username)
    except:
        root_object = Person.objects.create(full_name=instagram_username)
    friends = inst.get_friends_list_by_instagram_username(instagram_username)
    for root_friend in friends:
        try:
            try:
                root_friend_object = Person.objects.get(full_name=root_friend)
                continue
            except:
                root_friend_object = Person.objects.create(full_name=root_friend, parent=root_object)

            # friends_lvl_2 = inst.get_friends_list_by_instagram_username(root_friend)
            # for friend_lvl_2 in friends_lvl_2:
            #     try:
            #         try:
            #             friend_lvl_2_object = Person.objects.get(full_name=friend_lvl_2)
            #             continue
            #         except:
            #             friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
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