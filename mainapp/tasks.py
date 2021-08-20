from __future__ import absolute_import, unicode_literals
from conf.celery import app
from .main import InstagramStats
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

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


@app.task()
def get_instagram_friend_list_by_instagram_username(instagram_username):

    def get_friends_list_by_instagram_username(instagram_username):
        proxies = [
            '212.60.22.150:65233',
            '185.180.109.249:65233',
            '193.233.80.131:65233',
            '194.116.162.155:65233'
        ]

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()

        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size-1420,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        proxy_options = {
            'proxy': {
                'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
            }
        }

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                  seleniumwire_options=proxy_options)
        driver.get('https://www.instagram.com/')

        with open('/code/mainapp/cookies_jsons/cookie_inst.json', 'r', newline='') as inputdata:
            cookies = json.load(inputdata)
            for cookie in cookies:
                driver.add_cookie(cookie)

        time.sleep(get_random_number())
        driver.refresh()
        time.sleep(get_random_number())

        driver.implicitly_wait(60)
        driver.get(f'https://www.instagram.com/{instagram_username}/')

        followers = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]')
        followers.click()

        friends = set()
        try:
            driver.find_element_by_class_name('PZuss')
            pop_up_window = WebDriverWait(
                driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))
            i = 1
            fr = list()
            while True:
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                    pop_up_window)
                soup = bs(driver.page_source, 'html.parser')
                fr.append(len(soup.find_all('li', {"class": "wo9IH"})))
                if i % 10 == 0:
                    if len(set(fr)) == 1:
                        break
                    fr = []
                i += 1
                time.sleep(3)
        except:
            pass
        time.sleep(3)
        for element in soup.find_all(class_="FPmhX"):
            link = element.get('href')
            friends.add(link)

        driver.close()
        driver.quit()
        return del_slashes(friends)

    res = get_friends_list_by_instagram_username(instagram_username)
    print(res)
    print(len(res))

    return True


@app.task()
def get_instagram_person_stats_by_instagram_username(instagram_username):
    user = InstagramStats(username="", password="")
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
def get_vk_friend_list_by_vk_id(vk_id):
    access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
    root = vk_id


    def get_friends_list_by_vk_id(vk_id):
        get_vk_id_url = f'https://api.vk.com/method/users.get?user_ids={vk_id}&v=5.92&access_token={access_token}'
        get_vk_id = requests.get(get_vk_id_url).json()['response'][0]['id']
        get_user_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={get_vk_id}&fields=domain&v=5.92&access_token={access_token}'
        user_friends_list = requests.get(get_user_friends_list_url).json()['response']['items']
        return [friend['domain'] for friend in user_friends_list]


    for friend in get_friends_list_by_vk_id(root):
        try:
            print(friend, 'root person friend')
            print(get_friends_list_by_vk_id(friend))
            print()
        except:
            continue
        for friend_lvl_2 in get_friends_list_by_vk_id(friend):
            try:
                print(friend_lvl_2, 'friend lvl 2')
                print(get_friends_list_by_vk_id(friend_lvl_2))
                print()
            except:
                continue
            for friend_lvl_3 in get_friends_list_by_vk_id(friend_lvl_2):
                try:
                    print(friend_lvl_3, 'friend lvl 3')
                    print(get_friends_list_by_vk_id(friend_lvl_3))
                    print()
                except:
                    continue


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
