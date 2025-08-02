from django.contrib import admin
from .models import Thread, Answer
from accounts.models import CustomUser

admin.site.register(Thread)
admin.site.register(Answer)
admin.site.register(CustomUser)



