from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Friends)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(Dislikes)