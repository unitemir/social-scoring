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
    inst = Instagram('liudmilaorekhova4016', 'xUZFoGbPu8')
    inst.auth()
    print()
    root_object = Person.objects.create(full_name=instagram_username)
    friends = inst.get_friends_list_by_instagram_username(instagram_username)
    print(friends, "FRIENDS")
    for root_friend in friends:
        rf = Person.objects.create(full_name=root_friend)
        root_object.add_relationship(rf, 1)
    for root_friend in root_object.get_following():
        for friend_lvl_2 in inst.get_friends_list_by_instagram_username(root_friend.full_name):
            friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2)
            root_friend.add_relationship(friend_lvl_2_object, 1)
    inst.close_browser()
    print("a" * 55)
    return True


@app.task()
def create_vk_person_three(vk_id):
    access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
    root = vk_id

    def get_friends_list_by_vk_id(vk_id):
        get_vk_id_url = f'https://api.vk.com/method/users.get?user_ids={vk_id}&v=5.92&access_token={access_token}'
        get_vk_id = requests.get(get_vk_id_url).json()['response'][0]['id']
        get_user_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={get_vk_id}&fields=domain&v=5.92&access_token={access_token}'
        try:
            user_friends_list = requests.get(get_user_friends_list_url).json()['response']['items']
            return [friend['domain'] for friend in user_friends_list]
        except:
            return []

    root_object = Person.objects.create(full_name=root)

    for friend in get_friends_list_by_vk_id(root):
        try:
            root_friend_object = Person.objects.create(full_name=friend, parent=root_object)
        except:
            continue
        for friend_lvl_2 in get_friends_list_by_vk_id(friend):
            try:
                Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
            except:
                continue
    return True


@app.task()
def create_facebook_person_three(facebook_id):
    fb = Facebook()
    fb.auth()
    friends = fb.get_friends_list_by_face_book_id(facebook_id)
    root_object = Person.objects.create(username=facebook_id[1::], full_name=fb.object_name)
    for root_friend in friends:
        rf, created = Person.objects.get_or_create(username=friends[root_friend][1::], full_name=root_friend)
        root_object.add_relationship(rf, 1)
    for root_friend in root_object.get_following():
        print("ROOT FRIEND USERNAME:", root_friend.username)
        friends_f = fb.get_friends_list_by_face_book_id(root_friend.username)
        for friend_lvl_2 in friends_f:
            friend_lvl_2_object, created = Person.objects.get_or_create(username=friends_f[friend_lvl_2][1::], full_name=friend_lvl_2)
            root_friend.add_relationship(friend_lvl_2_object, 1)
    fb.driver_close()
    return True

