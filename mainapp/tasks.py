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


@app.task()
def get_instagram_friend_list_by_username(instagram_username):

    inst = Instagram('fevroniia8667', 'RmhPX76sq7')
    inst.auth()



    inst.close_browser()
    return True


# @app.task()
# def get_instagram_person_stats_by_instagram_username(instagram_username):
#     user = InstagramStats(username="", password="")
#     followers_len = user.get_followers_len(instagram_username)
#     total_len_posts = user.get_total_len_posts(instagram_username)
#     avr_likers = user.get_avr_likers(instagram_username)
#     avr_20_likers = user.get_20_avr_likers(instagram_username)
#     follwoing_len = user.get_follwoing_len(instagram_username)
#
#     new_user = Person.objects.create(
#         full_name='Instagram',
#         score=0,
#         qty_subscribers=followers_len,
#         subscriptions=follwoing_len,
#         qty_posts=total_len_posts,
#         avg_amount_likes_on_all_posts=avr_likers,
#         avg_amount_likes_on_last_20_posts=avr_20_likers
#     )
#
#     cookie_del = glob.glob("config/*cookie.json")
#     if cookie_del:
#         os.remove(cookie_del[0])
#
#     return True


@app.task()
def get_vk_friend_list_by_vk_id(vk_id):

    access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'

    def get_friends_list_by_vk_id(vk_id):
        get_vk_id_url = f'https://api.vk.com/method/users.get?user_ids={vk_id}&v=5.92&access_token={access_token}'
        get_vk_id = requests.get(get_vk_id_url).json()['response'][0]['id']
        get_user_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={get_vk_id}&fields=domain&v=5.92&access_token={access_token}'
        user_friends_list = requests.get(get_user_friends_list_url).json()['response']['items']
        return [friend['domain'] for friend in user_friends_list]

    try:
        root_object = Person.objects.get(full_name=vk_id)
    except:
        root_object = Person.objects.create(full_name=vk_id)

    for root_friend in get_friends_list_by_vk_id(vk_id):
        try:
            try:
                root_friend_object = Person.objects.get(full_name=root_friend)
            except:
                root_friend_object = Person.objects.create(full_name=root_friend, parent=root_object)

            for friend_lvl_2 in get_friends_list_by_vk_id(root_friend):
                try:
                    try:
                        friend_lvl_2_object = Person.objects.get(full_name=friend_lvl_2)
                    except:
                        friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
                except:
                    continue
        except:
            continue

    return True


# @app.task()
# def get_vk_person_stats_by_page_id():
#     new_user = Person.objects.create(
#         full_name='VK',
#         score=0,
#         qty_subscribers=qty_subscribers,
#         subscriptions=subscriptions,
#         qty_posts=qty_posts,
#         avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
#         avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
#     )
#     return True


@app.task()
def get_facebook_person_friend_list(facebook_id):
    fb = Facebook()
    fb.auth()
    friends = fb.get_friends_list_by_face_book_id(facebook_id)
    print(friends)
    print(len(friends))
    return True


# @app.task()
# def get_facebook_person_stats_by_facebook_id(facebook_id):
#
#     new_user = Person.objects.create(
#         full_name='facebook',
#         score=0,
#         qty_subscribers=number_of_friends,
#         subscriptions=number_of_friends,
#         qty_posts=len(valid_data),
#         avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
#         avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
#     )
#
#     driver.close()
#     driver.quit()
#
#     return True