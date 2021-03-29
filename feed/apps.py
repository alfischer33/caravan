from django.apps import AppConfig
#from feed.models import Vote
#from .signals import update_forum_score

class FeedConfig(AppConfig):
    name = 'feed'

    def ready(self):
        import feed.signals