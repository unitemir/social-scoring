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
        access_token = '23c80a4e23c80a4e23c80a4ee523b0e924223c823c80a4e42d9073819b94c55e72fc001'

        input_data = vk_id
        get_vk_user_id_url = f'https://api.vk.com/method/users.get?user_ids={input_data}&v=5.92&access_token={access_token}'
        vk_user_id = requests.get(get_vk_user_id_url).json()['response'][0]['id']

        get_user_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={vk_user_id}&fields=domain&v=5.92&access_token={access_token}'
        scammer_friends_list = requests.get(get_user_friends_list_url).json()['response']['items']

        data = {}

        scammer_model_object = Person.objects.create(username=input_data, score=1)

        for scammer_friend in scammer_friends_list:
            try:
                scammer_friend_model_object = Person.objects.get(username=scammer_friend['domain'])
            except:
                scammer_friend_model_object = Person.objects.create(username=scammer_friend['domain'], score=0.5, parent=scammer_model_object)
            scammer_friend_vk_domain = scammer_friend['domain']
            get_scammer_friend_vk_id_url = f'https://api.vk.com/method/users.get?user_ids={scammer_friend_vk_domain}&v=5.92&access_token={access_token}'
            scammer_friend_vk_id = requests.get(get_scammer_friend_vk_id_url).json()['response'][0]['id']
            data[scammer_friend_vk_domain] = []
            get_scammer_friend_friends_list_url = f'https://api.vk.com/method/friends.get?user_id={scammer_friend_vk_id}&fields=domain&v=5.92&access_token={access_token}'
            try:
                scammer_friend_friends_list = requests.get(get_scammer_friend_friends_list_url).json()['response'][
                    'items']
                for scammer_friend_friend in scammer_friend_friends_list:
                    try:
                        Person.objects.get(username=scammer_friend_friend['domain'])
                    except:
                        if scammer_friend_friend != input_data:
                            Person.objects.create(
                                username=scammer_friend_friend['domain'],
                                score=0.25,
                                parent=scammer_friend_model_object
                            )
                    data[scammer_friend_vk_domain].append(scammer_friend_friend['domain'])
            except:
                continue

        # scammer = input_data
        #
        # vertices = [scammer]
        #
        # for scammer_friend, scammer_friend_friends_list in data.items():
        #     vertices.append(scammer_friend)
        #     for scammer_friend_friend in scammer_friend_friends_list:
        #         if scammer_friend_friend == scammer:
        #             continue
        #         vertices.append(scammer_friend_friend)
        #
        # vertices.append(scammer)
        #
        # graph = {person: list() for person in vertices}

        # for friend, friend_friends in data.items():
        #     graph[scammer].append(friend)
        #     for friend_friend in friend_friends:
        #         if friend_friend == scammer:
        #             continue
        #         graph[friend].append(friend_friend)

        # print(graph)

        # visited = []
        # queue = []
        #
        # visited.append(scammer)
        # queue.append(scammer)
        #
        # while queue:
        #     s = queue.pop(0)
        #     for neighbour in graph[s]:
        #         if neighbour not in visited:
        #             visited.append(neighbour)
        #             queue.append(neighbour)

        return Response({'test': 'response'})


def show_persons(request):
    return render(request, "persons_three.html", {'persons': Person.objects.all()})