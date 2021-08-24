from rest_framework.views import APIView
from rest_framework.response import Response

from .tasks import *

from django.shortcuts import render


class GetSocialNetworksStatsView(APIView):

    def get(self, request, social_network, username):
        if social_network == 'Instagram':
            create_instagram_person_three.delay(username)
            return Response({'response': 'Instagram task has been running'})
        if social_network == 'Facebook':
            create_facebook_person_three.delay(username)
            return Response({'response': 'Facebook task has been running'})
        if social_network == 'VK':
            create_vk_person_three.delay(username)
            return Response({'response': 'VK task has been running'})


def show_persons(request):
    return render(request, "persons.html", {'persons': Person.objects.all()})