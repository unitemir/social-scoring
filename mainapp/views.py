from rest_framework.views import APIView

from django.http import HttpResponse

from .tasks import create_new_instagram_user, create_new_vk_person, get_facebook_friends_list, create_new_facebook_person
from rest_framework.response import Response

import requests
from django.shortcuts import render
from .models import Person


class CreateInstagramAPIView(APIView):

    def post(self, request, insta_username):
        create_new_instagram_user.delay(insta_username)
        return Response({'test': 'Instagram task has been running'})


class CreateVKPersonAPIView(APIView):

    def post(self, request, page_id):
        create_new_vk_person.delay(page_id)
        return Response({'test': 'VK task has been running'})


class CreateFacebookAPIView(APIView):

    def post(self, request, facebook_id):
        get_facebook_friends_list.delay(facebook_id)
        return Response({'test': 'Facebook task has been running'})



class GetVKScoreAPIView(APIView):

    def get(self, request, vk_id):
        input_data = vk_id
        get_user = f'https://api.vk.com/method/users.get?user_ids={input_data}&v=5.92&access_token=23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
        user_id = requests.get(get_user).json()['response'][0]['id']

        get_user_friedns = f'https://api.vk.com/method/friends.get?user_id={user_id}&fields=domain&v=5.92&access_token=23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'

        response = requests.get(get_user_friedns).json()['response']['items']

        scammer = input_data

        data = {}

        for friend in response:
            data[friend['domain']] = []
            inp_data = friend['domain']
            get_user = f'https://api.vk.com/method/users.get?user_ids={inp_data}&v=5.92&access_token=23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
            sub_flist = requests.get(get_user).json()['response'][0]['id']
            get_sub_flist_friedns = f'https://api.vk.com/method/friends.get?user_id={sub_flist}&fields=domain&v=5.92&access_token=23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'
            try:
                response = requests.get(get_sub_flist_friedns).json()
                response = response['response']['items']
                for sub_friend in response:
                    data[friend['domain']].append(sub_friend['domain'])
            except:
                continue

        print(data)

        for scammer_friend, scammer_friend_friends_list in data.items():
            print(scammer_friend_friends_list)

        # vertices = [scammer]
        #
        # for scammer_friend, scammer_friend_sub_friends in data.items():
        #     vertices.append(scammer_friend)
        #     for sub_friend in scammer_friend_sub_friends:
        #         if sub_friend == scammer:
        #             continue
        #         vertices.append(sub_friend)
        #
        # graph = {person: list() for person in vertices}
        #
        # for friend, sub_friends in data.items():
        #     for sub_friend in sub_friends:
        #         graph[friend].append(sub_friend)
        #         graph[sub_friend].append(friend)

        # print(graph)

        # start_vertex = scammer
        # queue = deque([start_vertex])
        # x = 0
        # while x < len(vertices):
        #     try:
        #         cur_v = queue.popleft()
        #     except:
        #         pass
        #
        #     if x == 1:
        #         for heigh_v in graph[cur_v]:
        #             try:
        #                 scammer_obj = Person.objects.get(name=cur_v)
        #             except:
        #                 scammer_obj = Person.objects.create(name=cur_v, score=1)
        #
        #             try:
        #                 Person.objects.get(name=heigh_v)
        #             except:
        #                 Person.objects.create(name=heigh_v, score=0.5, parent=scammer_obj)
        #
        #             queue.append(heigh_v)
        #
        #     print(x, cur_v)
        #
        #     for heigh_v in graph[cur_v]:
        #         print(heigh_v, 'heigh')
        #         queue.append(heigh_v)

        # start_vertex = scammer
        # queue = deque([start_vertex])
        # x = 0
        # while x < len(vertices):
        #     cur_v = queue.popleft()
        #     print(cur_v, 'cur_v')
        #     print(x)
        #
        #     for heigh_v in graph[cur_v]:
        #         print(heigh_v, 'heigh_v')
        #         queue.append(heigh_v)
        #     else:
        #         x += 1

        return Response({'status': 'success'})