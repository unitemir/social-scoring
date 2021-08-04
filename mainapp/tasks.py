from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import ChildBot
from .models import Person

import os
import glob

import json
import requests

access_token = 'a5dbc417f0806330df079ff23c2ce86f189e510811293df908842d07d0ff2ae797b1e7b4e2b334794889d'


@app.task()
def create_new_instagram_user(insta_username):
    user = ChildBot(username="tewovam682", password="Admin1234")
    followers_len = user.get_followers_len(insta_username)
    total_len_posts = user.get_total_len_posts(insta_username)
    avr_likers = user.get_avr_likers(insta_username)
    avr_20_likers = user.get_20_avr_likers(insta_username)
    follwoing_len = user.get_follwoing_len(insta_username)
    new_user = Person.objects.create(
        social_network='Instagram',
        qty_subscribers=followers_len,
        qty_posts=total_len_posts,
        avg_amount_likes_on_all_posts=avr_likers,
        avg_amount_likes_on_last_20_posts=avr_20_likers,
        subscriptions=follwoing_len
    )
    cookie_del = glob.glob("config/*cookie.json")
    if cookie_del:
        os.remove(cookie_del[0])
    return True


@app.task()
def create_new_vk_person(page_id):
    url = f'https://api.vk.com/method/users.get?user_ids={page_id}&v=5.92&access_token={access_token}'
    response = requests.get(url).json()
    user_id = response['response'][0]['id']
    avg_amount_likes_on_last_20_posts = 0
    url = f'https://api.vk.com/method/users.getFollowers?user_id={user_id}&count=1000&v=5.92&access_token={access_token}'
    r = requests.get(url)
    qty_subscribers = r.json()['response']['count']
    url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=100&v=5.92&access_token={access_token}'
    r = requests.get(url)
    qty_posts = r.json()['response']['count']
    url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=100&v=5.92&access_token={access_token}'
    r = requests.get(url)
    posts = r.json()
    likes = []
    last_20_likes = []
    for item in posts['response']['items']:
        likes.append(item['likes']['count'])
    else:
        avg_amount_likes_on_all_posts = sum(likes) / posts['response']['count']
    if posts['response']['count'] >= 20:
        for item in posts['response']['items'][:20]:
            last_20_likes.append(item['likes']['count'])
        else:
            avg_amount_likes_on_last_20_posts = sum(last_20_likes) / posts['response']['count']
    if posts['response']['count'] <= 20:
        pass
    url = f'https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&count=200&v=5.92&access_token={access_token}'
    r = requests.get(url)
    subscriptions = r.json()['response']['users']['count']
    new_user = Person.objects.create(
        social_network='VK',
        qty_subscribers=qty_subscribers,
        qty_posts=qty_posts,
        avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
        avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
        subscriptions=subscriptions
    )
    return True