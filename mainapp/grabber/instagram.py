from ..utils import *

import random
from datetime import datetime
import time

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


import os
import glob

from instabot import Bot

import requests

cookie_del = glob.glob("config/*cookie.json")
if cookie_del:
    os.remove(cookie_del[0])


class Instagram:

    def __init__(self, login, password, inst_username=None):

        self.login = login
        self.password = password
        self.inst_username = inst_username

        # proxies = [
        #     '212.60.22.150:65233',
        #     '185.180.109.249:65233',
        #     '193.233.80.131:65233',
        #     '194.116.162.155:65233'
        # ]

        # proxy_options = {
        #     'proxy': {
        #         'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
        #     }
        # }

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

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,
                                      ) #seleniumwire_options=proxy_options

    def auth(self):
        self.driver.get('https://instagram.com/')
        time.sleep(round(get_random_number(), 3))
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        self.driver.find_element_by_name('username').send_keys(self.login)
        passwd = self.driver.find_element_by_name('password')
        passwd.send_keys(self.password)
        passwd.send_keys(Keys.ENTER)
        time.sleep(5)

    def close_browser(self):
        self.driver.quit()

    def get_friends_list_by_instagram_username(self, inst_username):

        self.driver.implicitly_wait(60)
        self.driver.get(f'https://www.instagram.com/{inst_username}/')

        try:
            followers = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]')
            foll = followers.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span')
            if int(foll.text) > 500:
                return ['dalbaeb s 500 + podpiskami']
            followers.click()
        except:
            return []

        friends = set()
        try:
            self.driver.find_element_by_class_name('PZuss')
            pop_up_window = WebDriverWait(
                self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))
            i = 1
            fr = list()
            while True:
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                    pop_up_window)
                soup = bs(self.driver.page_source, 'html.parser')
                fr.append(len(soup.find_all('li', {"class": "wo9IH"})))
                if i % 10 == 0:
                    if len(set(fr)) == 1:
                        break
                    fr = []
                i += 1
                time.sleep(3)
        except:
            return []
        time.sleep(3)
        for elem in soup.find_all(class_='PZuss'):
            for el in elem.find_all('li'):
                for e in el.find_all('a'):
                    friends.add(e.get('href'))
        friends = set(friends)

        return del_slashes(friends)


class InstagramStats:
    def __init__(self, username, password):
        self.bot = Bot()
        self.bot.login(username=username, password=password)

    def get_username(self, full_name, n=0):
        username = self.bot.search_users(full_name)[n]
        return username

    def get_follwoing_len(self, username):
        return len(self.bot.get_user_following(username))

    def get_followers_len(self, username):
        return len(self.bot.get_user_followers(username))

    def get_total_len_posts(self, username):
        return len(self.bot.get_total_user_medias(username))

    def get_avr_likers(self, username):
        avr_likers = []
        total_medias = self.bot.get_total_user_medias(username)
        if total_medias:
            for i in range(len(total_medias)):
                liked = self.bot.get_media_likers(total_medias[i])
                avr_likers.append(len(liked))
            avr_likers = sum(avr_likers) / len(avr_likers)
        return avr_likers

    def get_20_avr_likers(self, username):
        twony_last_medias = self.bot.get_user_medias(username, filtration=None)
        twony_avr_likers = []
        if twony_last_medias:
            for media in twony_last_medias:
                liked = self.bot.get_media_likers(media)
                twony_avr_likers.append(len(liked))
            twony_avr_likers = sum(twony_avr_likers) / len(twony_avr_likers)
        return twony_avr_likers

    def download_photo(self, media_id, filename):
        media = self.bot.get_media_info(media_id)[0]
        if "image_versions2" in media.keys():
            url = media["image_versions2"]["candidates"][0]["url"]
            response = requests.get(url)
            with open(filename + ".jpg", "wb") as f:
                response.raw.decode_content = True
                f.write(response.content)
        elif "carousel_media" in media.keys():
            for e, element in enumerate(media["carousel_media"]):
                url = element['image_versions2']["candidates"][0]["url"]
                response = requests.get(url)
                with open(filename + str(e) + ".jpg", "wb") as f:
                    response.raw.decode_content = True
                    f.write(response.content)

    def download_last_5_posts(self, username):
        twony_last_medias = self.bot.get_user_medias(username, filtration=None)
        for e, media_id in enumerate(twony_last_medias):
            self.download_photo(media_id, "img_" + str(e))