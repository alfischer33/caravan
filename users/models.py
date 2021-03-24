from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.urls import reverse #unnecessary

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    nationality = models.CharField(max_length=63, blank=True)
    age = models.IntegerField(null=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return f"/users/{self.slug}"

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: From {self.from_user.username}, to {self.to_user.username}"