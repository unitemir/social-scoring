from django.contrib import admin
from .models import *


admin.site.register(Person)
admin.site.register(PersonStats)
admin.site.register(InstagramAccount)
admin.site.register(FacebookAccount)
admin.site.register(Proxy)