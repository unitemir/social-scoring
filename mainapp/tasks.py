from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import ChildBot
from .models import Person

import os
import glob

import json
import requests
import re

access_token = 'a5dbc417f0806330df079ff23c2ce86f189e510811293df908842d07d0ff2ae797b1e7b4e2b334794889d'


from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import time

from random import randint, random


def get_random_number():
    return randint(4, 15) * random()


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


@app.task()
def get_facebook_friends_list(facebook_id):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://m.facebook.com/')

    login = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')
    btn = driver.find_element_by_name('login')

    time.sleep(get_random_number())
    login.send_keys('efwiw23rr44t5@yandex.kz')
    time.sleep(get_random_number())
    password.send_keys('swudihf2398yr3484t')
    time.sleep(get_random_number())
    btn.click()

    time.sleep(get_random_number() + 2)
    btn1 = driver.find_element_by_class_name('_4g34')
    btn1.click()
    time.sleep(get_random_number())
    driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')
    time.sleep(get_random_number())

    number_of_friends = 0
    data = []
    ########### поиск кол друзей ###########
    time.sleep(get_random_number())
    elemnt_name = driver.find_element_by_class_name('_7-1j')
    number_of_friends = re.findall('(\d+)', elemnt_name.text)[0]
    print(number_of_friends)
    #####################
    time.sleep(get_random_number())
    elemnt_name.click()
    time.sleep(get_random_number())

    total_friends = dict()

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(get_random_number())
        elemnts_name = driver.find_elements_by_class_name('_84l2')

        # Wait to load page
        time.sleep(get_random_number())

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    for element in elemnts_name:
        total_friends[element.text] = element.find_element_by_tag_name("a").get_attribute("href")
    print(total_friends)
    time.sleep(24)
    driver.close()
    return number_of_friends


@app.task()
def create_new_facebook_person(facebook_id):

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.facebook.com/')

    login = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')
    btn = driver.find_element_by_name('login')

    login.send_keys('efwiw23rr44t5@yandex.kz')
    time.sleep(get_random_number())
    password.send_keys('swudihf2398yr3484t')
    time.sleep(get_random_number())
    btn.click()

    time.sleep(get_random_number())
    driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')
    time.sleep(get_random_number())

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    valid_data = []
    # qty_posts = 0

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(get_random_number())
        likes_class = driver.find_elements_by_class_name('_1g06')
        for i in likes_class:
            try:
                integer = int(i.text)
                valid_data.append(integer)
            except:
                pass

        time.sleep(get_random_number())
        # class_feed = driver.find_element_by_class_name('feed')
        # section_class = class_feed.find_element_by_tag_name('section')
        # articles = section_class.find_elements_by_tag_name('article')
        # for article in articles:
        #     print(article)
        #     qty_posts += 1

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    try:
        avg_amount_likes_on_all_posts = sum(valid_data) / len(valid_data)
        # print(avg_amount_likes_on_all_posts)

        if len(valid_data) >= 20:
            avg_amount_likes_on_last_20_posts = sum(valid_data[:20]) / 20
            # print(avg_amount_likes_on_last_20_posts)
        if len(valid_data) <= 20:
            avg_amount_likes_on_last_20_posts = avg_amount_likes_on_all_posts
            # print(avg_amount_likes_on_all_posts)
        # print(len(valid_data))
    except:
        pass

    new_user = Person.objects.create(
        social_network='FACEBOOK',
        qty_subscribers=0,
        qty_posts=len(valid_data),
        avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
        avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
        subscriptions=0
    )
    return True