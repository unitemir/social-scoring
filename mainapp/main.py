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