from rest_framework.views import APIView

from django.http import HttpResponse

from .tasks import *
from rest_framework.response import Response

import requests
from django.shortcuts import render
from .models import Person


class GetSocialNetworksStatsView(APIView):

    def get(self, request, social_network, username):
        if social_network == 'Instagram':
            create_new_instagram_user.delay(username)
            return Response({'test': 'Instagram task has been running'})
        if social_network == 'Facebook':
            get_friends.delay(username)
            return Response({'test': 'Facebook task has been running'})
        if social_network == 'VK':
            create_new_vk_person.delay(username)
            return Response({'test': 'VK task has been running'})