from django.contrib import admin
from .models import Caravan, Stop, Destination, Government, Forum, Vote

# Register your models here.
admin.site.register(Caravan)
admin.site.register(Stop)
admin.site.register(Destination)
admin.site.register(Government)
admin.site.register(Forum)
admin.site.register(Vote)