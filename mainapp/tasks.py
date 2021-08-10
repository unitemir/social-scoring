from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import ChildBot
from .models import Person

import os
import glob

import json
import requests
import re

access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'


from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

import time

from random import randint, random

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


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

    chrome_options = Options()

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size-1420,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    driver.get('https://m.facebook.com/')

    login = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')
    btn = driver.find_element_by_name('login')

    time.sleep(get_random_number())
    login.send_keys('87087653537')
    time.sleep(get_random_number())
    password.send_keys('test4321')
    time.sleep(get_random_number())
    btn.click()

    time.sleep(get_random_number())
    btn1 = driver.find_element_by_class_name('_4g34')
    btn1.click()
    time.sleep(get_random_number())
    driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}&sk=friends&__nodl')
    time.sleep(get_random_number())

    number_of_friends = 0
    data = []

    try:
        ########### поиск кол друзей ###########
        time.sleep(get_random_number())
        elemnt_name = driver.find_element_by_class_name('_7-1j')
        number_of_friends = re.findall('(\d+)', elemnt_name.text)[0]
        # print(number_of_friends)

        time.sleep(get_random_number())
        elemnt_name.click()
        time.sleep(get_random_number())
        #####################
        # time.sleep(get_random_number())
        # elemnt_name.click()
        # time.sleep(get_random_number())
        #
        # total_friends = dict()
        #
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # while True:
        #     # Scroll down to bottom
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #
        #     time.sleep(get_random_number())
        #     elemnts_name = driver.find_elements_by_class_name('_84l2')
        #
        #     # Wait to load page
        #     time.sleep(get_random_number())
        #
        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         breakexcept
        #     last_height = new_height
        # for element in elemnts_name:
        #     total_friends[element.text] = element.find_element_by_tag_name("a").get_attribute("href")
        # print(total_friends)
    except:
        number_of_friends = 0
        return create_new_facebook_person(facebook_id, number_of_friends)
    driver.close()
    driver.quit()
    return create_new_facebook_person(facebook_id, number_of_friends)


@app.task()
def create_new_facebook_person(facebook_id, number_of_friends):

    chrome_options = Options()

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value,
                         OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size-1420,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.maximize_window()
    driver.get('https://www.facebook.com/')

    login = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')
    btn = driver.find_element_by_name('login')

    login.send_keys('87087653537')
    time.sleep(get_random_number())
    password.send_keys('test4321')
    time.sleep(get_random_number())
    btn.click()

    time.sleep(get_random_number())
    driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')
    time.sleep(get_random_number())

    last_height = driver.execute_script("return document.body.scrollHeight")

    valid_data = []

    avg_amount_likes_on_all_posts = 0
    avg_amount_likes_on_last_20_posts = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    try:
        avg_amount_likes_on_all_posts = sum(valid_data) / len(valid_data)
        if len(valid_data) >= 20:
            avg_amount_likes_on_last_20_posts = sum(valid_data[:20]) / 20
        if len(valid_data) <= 20:
            avg_amount_likes_on_last_20_posts = avg_amount_likes_on_all_posts
    except:
        pass

    new_user = Person.objects.create(
        social_network='Facebook',
        qty_subscribers=0,
        qty_posts=len(valid_data),
        avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
        avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
        subscriptions=0
    )
    driver.close()
    driver.quit()
    return True