from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import InstagramStats
from .models import Person
from .utils import get_random_number

import os
import re
import time
import requests
import json
import glob

from random import choice

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@app.task()
def get_instagram_person_stats_by_instagram_username(instagram_username):
    user = InstagramStats(username="tewovam682", password="Admin1234")
    followers_len = user.get_followers_len(instagram_username)
    total_len_posts = user.get_total_len_posts(instagram_username)
    avr_likers = user.get_avr_likers(instagram_username)
    avr_20_likers = user.get_20_avr_likers(instagram_username)
    follwoing_len = user.get_follwoing_len(instagram_username)

    new_user = Person.objects.create(
        full_name='Instagram',
        score=0,
        qty_subscribers=followers_len,
        subscriptions=follwoing_len,
        qty_posts=total_len_posts,
        avg_amount_likes_on_all_posts=avr_likers,
        avg_amount_likes_on_last_20_posts=avr_20_likers
    )

    cookie_del = glob.glob("config/*cookie.json")
    if cookie_del:
        os.remove(cookie_del[0])

    return True


@app.task()
def get_vk_person_stats_by_page_id(page_id):
    access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
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
        full_name='VK',
        score=0,
        qty_subscribers=qty_subscribers,
        subscriptions=subscriptions,
        qty_posts=qty_posts,
        avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
        avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
    )
    return True


@app.task()
def get_facebook_person_friend_list(facebook_id):

    user_agents = [
        'Mozilla/5.0 (Linux Android 10 M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 7.1.2 Redmi Note 5A Prime Build/N2G47H wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 7.0 SAMSUNG SM-G928F/G928FXXS5CRH1) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 10 RMX2020 Build/QP1A.190711.020 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36',
    ]

    proxies = [
        '212.60.22.150:65233',
        '185.180.109.249:65233',
        '193.233.80.131:65233',
        '194.116.162.155:65233'
    ]

    cookies_files = ['/code/mainapp/cookies_jsons/cookie2.json']

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size-1420,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent={choice(user_agents)}')
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    proxy_options = {
        'proxy': {
            'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
        }
    }

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, seleniumwire_options=proxy_options)

    driver.maximize_window()
    driver.get('https://m.facebook.com/')

    with open(f'{choice(cookies_files)}', 'r', newline='') as inputdata:
        cookies = json.load(inputdata)
        for cookie in cookies:
            driver.add_cookie(cookie)

    time.sleep(get_random_number())
    driver.refresh()
    time.sleep(get_random_number())

    driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')

    try:
        total_friends = dict()
        time.sleep(get_random_number())
        elements_name = driver.find_element_by_class_name('_7-1j')
        number_of_friends = int(''.join(elements_name.text.split()[1:]))
        if number_of_friends > 1000:
            return number_of_friends

        elements_name.click()
        time.sleep(get_random_number())

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            time.sleep(get_random_number())
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(get_random_number())
            elements_name = driver.find_elements_by_class_name('_84l2')
            for element in elements_name:
                total_friends[element.text] = element.find_element_by_tag_name("a").get_attribute("href")
            time.sleep(get_random_number())
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # print(len(total_friends))
        return total_friends
    except:
        return 0
    finally:
        driver.close()
        driver.quit()


@app.task()
def get_facebook_person_stats_by_facebook_id(facebook_id, number_of_friends):
    user_agents = [
        'Mozilla/5.0 (Linux Android 10 M2006C3MG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 7.1.2 Redmi Note 5A Prime Build/N2G47H wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.87 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 7.0 SAMSUNG SM-G928F/G928FXXS5CRH1) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux Android 10 RMX2020 Build/QP1A.190711.020 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36',
    ]

    proxies = [
        '212.60.22.150:65233',
        '185.180.109.249:65233',
        '193.233.80.131:65233',
        '194.116.162.155:65233'
    ]

    cookies_files = ['/code/mainapp/cookies_jsons/cookie2.json', '/code/mainapp/cookies_jsons/cookietest.json']

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size-1420,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent={choice(user_agents)}')
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    proxy_options = {
        'proxy': {
            'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
        }
    }

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                              seleniumwire_options=proxy_options)

    driver.maximize_window()
    driver.get('https://m.facebook.com/')

    with open(f'{choice(cookies_files)}', 'r', newline='') as inputdata:
        cookies = json.load(inputdata)
        for cookie in cookies:
            driver.add_cookie(cookie)

    time.sleep(get_random_number())
    driver.refresh()
    time.sleep(get_random_number())

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
        full_name='facebook',
        score=0,
        qty_subscribers=number_of_friends,
        subscriptions=number_of_friends,
        qty_posts=len(valid_data),
        avg_amount_likes_on_all_posts=avg_amount_likes_on_all_posts,
        avg_amount_likes_on_last_20_posts=avg_amount_likes_on_last_20_posts,
    )

    driver.close()
    driver.quit()

    return True
