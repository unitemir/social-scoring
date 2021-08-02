from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import ChildBot
from .models import InstagramUser

import os
import glob


@app.task()
def create_new_instagram_user(insta_username):
    user = ChildBot(username="tewovam682", password="Admin1234")
    followers_len = user.get_followers_len(insta_username)
    total_len_posts = user.get_total_len_posts(insta_username)
    avr_likers = user.get_avr_likers(insta_username)
    avr_20_likers = user.get_20_avr_likers(insta_username)
    follwoing_len = user.get_follwoing_len(insta_username)
    new_user = InstagramUser.objects.create(
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