from rest_framework.views import APIView

from django.http import HttpResponse

from .tasks import create_new_instagram_user, create_new_vk_person


class CreateInstagramAPIView(APIView):

    def post(self, request, insta_username):
        create_new_instagram_user.delay(insta_username)
        return HttpResponse('OK')


class CreateVKPersonAPIView(APIView):

    def post(self, request, page_id):
        create_new_vk_person.delay(page_id)
        return HttpResponse('OK')

