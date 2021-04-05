from django.db import models
from django.contrib.auth.models import User
import datetime
from autoslug import AutoSlugField

class Caravan(models.Model):
    name = models.CharField(max_length=127, unique=True)
    description = models.CharField(max_length=1023, blank=True)
    tags = models.CharField(max_length=511, blank=True)
    creator = models.ForeignKey(User, related_name='caravan_creator', null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField(default=datetime.date.today())
    members = models.ManyToManyField(User, blank=True, related_name='caravans')
    parent_caravan = models.ForeignKey('caravan', null=True, blank=True, on_delete=models.SET_NULL),
    private = models.BooleanField(default=False)
    invisible = models.BooleanField(default=False)
    allow_member_stop_proposals = models.BooleanField(default=True)
    blocked_users = models.ManyToManyField(User, blank=True, related_name='blocked')
    flexible_dates = models.BooleanField(default=False) #only define current stop end date once stop begun

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

    youngadults = '18-23'
    quarterlife = '23-29'
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

    def advance_queue(self):
        stops = Stop.objects.filter(caravan=self).all()
        if stops.get(stop_queue_position=0).end_date < datetime.date.today():
            for stop in stops:
                stop.advance_queue_position()
        return
    

class Stop(models.Model):
    caravan = models.ForeignKey('caravan',on_delete=models.CASCADE)
    destination = models.ForeignKey('destination',on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, blank=True)
    description = models.CharField(max_length=511, blank=True)
    end_date = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='caravan', unique=True)
    stop_queue_position = models.IntegerField(blank=True, null=True) # -1 is previous stop, 0 is current stop, 1 is next stop, blank is unchosen stop

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
        return f'{self.caravan} stop at {self.destination}: Queue {self.stop_queue_position}'

    def get_absolute_url(self):
        return f"/feed/stop/{self.slug}"

    def update_slug(self):
        self.save()
        print(f'Slug updated to {self.slug}')
        returnd

    def advance_queue_position(self):
        if self.stop_queue_position != 1:
            self.stop_queue_position = self.stop_queue_position - 1
        else:
            if self.status == self.proposal:
                self.stop_queue_position = None
            else:
                self.stop_queue_position = 0
        self.save()
        return self

# class EventStop(Stop):
#     start_date = models.DateField()


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
    rating = models.FloatField(default=0)
# AccommodationDestination (Hotels, etc.), CampDestination


class Government(models.Model):
    caravan = models.OneToOneField('caravan', on_delete=models.CASCADE)
    leaders = models.ManyToManyField(User)  
    leader_vote_multiplier = models.FloatField(default=1)
    legacy_vote_multiplier = models.FloatField(default=1)
    member_vote_multiplier = models.FloatField(default=0)
    public_ballots = models.BooleanField(default=True)
    vote_against = models.BooleanField(default=False)
    legacy_threshold = models.IntegerField(default=2)
    leader_checkins = models.BooleanField(default=True)
    legacy_checkins = models.BooleanField(default=False)
    open_checkins = models.BooleanField(default=False)
    show_interest_score = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.caravan} government'

    @classmethod
    def create_standand(cls, c_name):
        govt = cls(caravan=Caravan.objects.filter(name=c_name).first())
        return govt
    
    @classmethod
    def create_guided(cls, c_name):
        govt = cls(caravan=Caravan.objects.filter(name=c_name).first())
        govt.legacy_vote_multiplier = 0
        govt.public_ballots = False
        govt.legacy_threshold = 1
        return govt

    @classmethod
    def create_open(cls, c_name):
        govt = cls(caravan=Caravan.objects.filter(name=c_name).first())
        govt.public_ballots = True
        govt.legacy_threshold = 1
        govt.open_checkins = True
        govt.legacy_checkins = True
        govt.vote_against = False
        return govt


class Forum(models.Model):
    resolved = models.BooleanField(default=False)
    government = models.ForeignKey('government', on_delete=models.CASCADE)
    description = models.CharField(max_length=511, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.government) + " " + str(self.id)

class StopForum(Forum):
    stop = models.OneToOneField('stop', on_delete=models.CASCADE)

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

    def __str__(self):
        return str(self.user) + (' for ' if self.infavor else ' against ') + str(self.forum)

    @classmethod
    def create_yes(cls, user, forum):
        v = cls(user=user, forum=forum, infavor=True)
        return v