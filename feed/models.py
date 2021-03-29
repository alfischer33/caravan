from django.db import models
from django.contrib.auth.models import User
import datetime
from autoslug import AutoSlugField

class Caravan(models.Model):
    name = models.CharField(max_length=127, unique=True)
    description = models.CharField(max_length=1023, blank=True)
    tags = models.CharField(max_length=511, blank=True)
    creator = models.ForeignKey(User, related_name='caravan_creator', null=True, blank=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, blank=True, related_name='caravans')
    parent_caravan = models.ForeignKey('caravan', null=True, blank=True, on_delete=models.SET_NULL),
    split_date = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    invisible = models.BooleanField(default=False)
    allow_member_stop_proposals = models.BooleanField(default=True)
    blocked_users = models.ManyToManyField(User, blank=True, related_name='blocked')

    event = 'event'
    journey = 'journey'
    nomadic = 'nomadic'
    other = 'other'
    duration_choices = (
        (event, 'Event'),
        (journey, 'Journey'),
        (nomadic, 'Nomadic'),
        (other, 'Other')
    )
    duration = models.CharField(max_length=15, choices=duration_choices)

    party = 'party'
    enjoy = 'enjoy'
    explore = 'explore'
    volunteer = 'volunteer'
    work = 'work'
    other = 'other'
    mood_choices = (
        (party, 'Party'),
        (enjoy, 'Enjoy'),
        (explore, 'Explore'),
        (volunteer, 'Volunteer'),
        (work, 'Work'),
        (other, 'Other')
    )
    mood = models.CharField(max_length=15, choices=mood_choices)

    youngadults = '18-25'
    quarterlife = '25-29'
    thirties = '30-39'
    midlife = '40-65'
    seniors = '65+'
    any_age = 'any'
    family = 'family'
    age_choices = (
        (youngadults, '18-23'),
        (quarterlife, '23-29'),
        (thirties, '30-39'),
        (midlife, '40-65'),
        (seniors, '65+'),
        (family, 'Family'),
        (any_age, 'All Ages')
    )
    age_range = models.CharField(max_length=15, choices=age_choices)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f"/feed/caravan/{self.name}"

    def tag_list(self):
        return self.tags.split('#,').str.strip()
    
class Stop(models.Model):
    caravan = models.ForeignKey('caravan',on_delete=models.CASCADE)
    destination = models.ForeignKey('destination',on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, blank=True)
    description = models.CharField(max_length=511, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    private = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='caravan', unique=True)

    decided = 'decided'
    tentative = 'tentative'
    proposal = 'proposal'
    status_choices = (
        (decided, 'Decided'),
        (tentative, 'Tentative'),
        (proposal, 'Proposal')
    )
    status = models.CharField(max_length=15, choices=status_choices, default=proposal)

    def __str__(self):
        return f'{self.caravan} stop at {self.destination}: {self.start_date} to {self.end_date}'

    def get_absolute_url(self):
        return f"/feed/stop/{self.slug}"

    def update_slug(self):
        self.save()
        print(f'Slug updated to {self.slug}')
        return

class Destination(models.Model):
    name = models.CharField(max_length=127)
    link = models.URLField()
    description = models.CharField(max_length=511, blank=True)

    def __str__(self):
        return str(self.name)

class AreaDestination(Destination):
    location = models.CharField(max_length=127)
class EventDestination(Destination):
    event_name = models.CharField(max_length=31)
class HostelDestination(Destination):
    rating = models.FloatField()
# AccommodationDestination (Hotels, etc.), CampDestination

class Government(models.Model):
    caravan = models.OneToOneField('caravan', on_delete=models.CASCADE)
    leaders = models.ManyToManyField(User)  
    leader_vote_multiplier = models.FloatField(default=1)
    legacy_vote_multiplier = models.FloatField(default=0)
    member_vote_multiplier = models.FloatField(default=1)
    public_ballots = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.caravan} government'

    @classmethod
    def create_standand(cls, c_name):
        govt = cls(caravan=Caravan.objects.filter(name=c_name).first())
        return govt


class Forum(models.Model):
    resolved = models.BooleanField(default=False)
    government = models.ForeignKey('government', on_delete=models.CASCADE)
    description = models.CharField(max_length=511, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    score = models.IntegerField(default=0)

class StopForum(Forum):
    stop = models.ForeignKey('stop', on_delete=models.CASCADE)

    @classmethod
    def from_stop(cls, s):
        sf = cls(   
            stop=s, 
            government=Government.objects.filter(caravan=s.caravan).first(), 
            description=s.description, 
            deadline=s.start_date - datetime.timedelta(days=7))
        return sf

    def __str__(self):
        return str(self.stop) + ' forum'

class AddLeaderForum(Forum):
    new_leader = models.ForeignKey(User, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #this should be deleted if the user leaves the group
    forum = models.ForeignKey('forum', on_delete=models.CASCADE, null=True)
    infavor = models.BooleanField()