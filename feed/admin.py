from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Caravan)
admin.site.register(Stop)
admin.site.register(Destination)
admin.site.register(Government)
admin.site.register(StopForum)
admin.site.register(Vote)