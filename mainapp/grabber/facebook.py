
import json
import time

from random import randint, random, choice, uniform
from seleniumwire import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
def get_random_number():
    return random() * randint(3, 15)


class Facebook:

    def __init__(self, fb_username=None):
        self.fb_username = fb_username
        self.total_friends = dict()
        self.object_name = ''
        # proxies = [
        #     '212.60.22.150:65233',
        #     '185.180.109.249:65233',
        #     '193.233.80.131:65233',
        #     '194.116.162.155:65233'
        # ]
        #
        # proxy_options = {
        #     'proxy': {
        #         'https': f'https://3010egh:J9g8TdC@{choice(proxies)}',
        #     }
        # }

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.ANDROID.value]
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

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options,)

    def auth(self):
        self.driver.get('https://m.facebook.com/')
        # cookies_files = ['/code/mainapp/cookies_jsons/cookie2.json']
        # with open(f'{choice(cookies_files)}', 'r', newline='') as inputdata:
        #     cookies = json.load(inputdata)
        #     for cookie in cookies:
        #         self.driver.add_cookie(cookie)
        # self.driver.refresh()
        time.sleep(uniform(2, 10))
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'email')))
        self.driver.find_element_by_name('email').send_keys("aktai.t@mail.ru")
        passwd = self.driver.find_element_by_name('pass')
        time.sleep(uniform(2, 10))
        passwd.send_keys("banan123")
        passwd.send_keys(Keys.ENTER)
        time.sleep(uniform(2, 10))

    def driver_close(self):
        self.driver.close()
        self.driver.quit()

    def get_friends_list_by_face_book_id(self, face_book_id):
        time.sleep(uniform(3, 7))
        self.driver.get(f"https://m.facebook.com/{face_book_id}")
        time.sleep(get_random_number())
        self.object_name = self.driver.find_element_by_class_name("_6x2x")
        self.object_name = self.object_name.text
        time.sleep(get_random_number())
        try:
            element = self.driver.find_element_by_class_name('_7-1j')#"/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[1]/div/div/a/div/div[2]"
        except:
            return {}
        try:
            number_of_friends = element.text.split()[1]
            if number_of_friends > 1000:
                return {}
        except:
            pass
        element.click()

        time.sleep(get_random_number())
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            time.sleep(uniform(2, 10))
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(uniform(2, 10))
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        soup = bs(self.driver.page_source, 'html.parser')
        for elem in soup.find_all(class_='_84l2'):
            for el in elem.find_all('a'):
                self.total_friends[el.text.strip()] = el.get('href').removeprefix("https://www.facebook.com/")
        return self.total_friends

    def get_valid_data(self):
        # driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')
        valid_data = []
        last_height = driver.execute_script("return document.body.scrollHeight")
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
            return valid_data

    def get_avg_likes_on_posts(self):
        avg_amount_likes_on_all_posts = 0
        avg_amount_likes_on_last_20_posts = 0
        try:
            avg_amount_likes_on_all_posts = sum(valid_data) / len(valid_data)
            if len(valid_data) >= 20:
                avg_amount_likes_on_last_20_posts = sum(valid_data[:20]) / 20
            if len(valid_data) <= 20:
                avg_amount_likes_on_last_20_posts = avg_amount_likes_on_all_posts
        except:
            pass
        return