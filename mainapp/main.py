import os
import glob

from instabot import Bot

import requests

cookie_del = glob.glob("config/*cookie.json")
if cookie_del:
    os.remove(cookie_del[0])


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


class VKStats:

    def __init__(self, page_id):
        self.access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
        self.page_id = page_id

    def get_user_id(self):
        url = f'https://api.vk.com/method/users.get?user_ids={self.page_id}&v=5.92&access_token={self.access_token}'
        response = requests.get(url).json()
        return response['response'][0]['id']

    def get_avg_amount_likes_on_last_20_posts(self):
        pass

    def get_qty_subscribers(self):
        url = f'https://api.vk.com/method/users.getFollowers?user_id={user_id}&count=1000&v=5.92&access_token={access_token}'
        r = requests.get(url)
        return r.json()['response']['count']

    def get_qty_posts(self):
        url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=100&v=5.92&access_token={access_token}'
        r = requests.get(url)
        return r.json()['response']['count']

    def get_subscriptions_qty(self):
        url = f'https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&count=200&v=5.92&access_token={access_token}'
        r = requests.get(url)
        return r.json()['response']['users']['count']

    # def get_avg_amount_likes_on_all_posts(self):
    #     avg_amount_likes_on_last_20_posts = 0
    #     url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=100&v=5.92&access_token={access_token}'
    #     r = requests.get(url)
    #     posts = r.json()
    #     likes = []
    #     last_20_likes = []
    #     for item in posts['response']['items']:
    #         likes.append(item['likes']['count'])
    #     else:
    #         avg_amount_likes_on_all_posts = sum(likes) / posts['response']['count']
    #     if posts['response']['count'] >= 20:
    #         for item in posts['response']['items'][:20]:
    #             last_20_likes.append(item['likes']['count'])
    #         else:
    #             avg_amount_likes_on_last_20_posts = sum(last_20_likes) / posts['response']['count']
    #     if posts['response']['count'] <= 20:
    #         pass


class FacebookStats:

    def __init__(self):
        # driver.get(f'https://m.facebook.com/profile.php?id={facebook_id}')
        pass

    def get_valid_data(self):
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