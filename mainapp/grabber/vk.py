class VK:
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