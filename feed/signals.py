from .models import Vote, Forum, Caravan, Government
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Vote)
def update_forum_score(sender, instance, **kwargs):
    f = instance.forum
    print(f'previous forum score: {f.score}')
    f.score = Vote.objects.filter(forum=f).count()
    f.save()
    print(f'New forum score: {f.score}')

# @receiver(post_save, sender=Caravan)
# def create_caravan_govt(sender, instance, **kwargs):
