from django import forms
from .models import Caravan, Stop, Government

class CaravanCreateForm(forms.ModelForm):
    
    class Meta:
        model = Caravan
        fields = ['name', 'description', 'tags', 'duration', 'mood', 'age_range', 'private']

class GovernmentUpdateForm(forms.ModelForm):

    class Meta:
        model = Government
        fields = ['leaders', 'leader_vote_multiplier', 'legacy_vote_multiplier', 'member_vote_multiplier', 'public_ballots']

class StopCreateForm(forms.ModelForm):
    
    class Meta:
        model = Stop
        fields = ['caravan', 'destination', 'description', 'start_date', 'end_date', 'private']