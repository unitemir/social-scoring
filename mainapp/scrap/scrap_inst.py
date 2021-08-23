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

        # proxy_options = {
        #     'proxy': {
        #         'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
        #     }
        # }

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)#, seleniumwire_options=proxy_options


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
            pass
        time.sleep(3)
        for elem in soup.find_all(class_='PZuss'):
            for el in elem.find_all('li'):
                for e in el.find_all('a'):
                    friends.add(e.get('href'))
        friends = set(friends)

        return del_slashes(friends)