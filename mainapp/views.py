from rest_framework.views import APIView
from rest_framework.response import Response

from .tasks import *


class GetSocialNetworksStatsView(APIView):

    def get(self, request, social_network, username):
        if social_network == 'Instagram':
            # create_new_instagram_user.delay(username)
            # return Response({'response': 'Instagram task has been running'})
            pass
        if social_network == 'Facebook':
            get_facebook_person_friend_list.delay(username)
            return Response({'response': 'Facebook task has been running'})
        if social_network == 'VK':
            # create_new_vk_person.delay(username)
            # return Response({'response': 'VK task has been running'})
            pass