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


@app.task()
def create_instagram_person_three(instagram_username):
    inst = Instagram('fevroniia8667', 'RmhPX76sq7')
    inst.auth()
    inst.close_browser()
    return True


@app.task()
def create_vk_person_three(vk_id):
    print('asd')
    return vk_id


@app.task()
def create_facebook_person_three(facebook_id):
    fb = Facebook()
    fb.auth()
    friends = fb.get_friends_list_by_face_book_id(facebook_id)
    print(friends)
    print(len(friends))
    return True