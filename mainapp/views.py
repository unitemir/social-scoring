from rest_framework.views import APIView

from django.http import HttpResponse

from .tasks import create_new_instagram_user


class CreateInstagramAPIView(APIView):

    def post(self, request, insta_username):
        create_new_instagram_user.delay(insta_username)
        return HttpResponse('OK')
