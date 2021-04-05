from .models import *
from .forms import CaravanCreateForm, GovernmentUpdateForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

def caravan(request, name):

    u = request.user
    c = Caravan.objects.filter(name=name).first()
    ismember = request.user in c.members.all()
    stops = Stop.objects.filter(caravan=c).all()

    #https://www.abidibo.net/blog/2014/05/22/check-if-user-belongs-group-django-templates/

    begun = c.start_date <= datetime.date.today()
    first_forum = stops.first().stopforum

    context={"c":c, "ismember":ismember, "stops":stops, "begun":begun}
    
    return render(request, 'feed/caravan.html', context)

def caravan_list(request):

    all_caravans = Caravan.objects.all()

    my_stops = Stop.objects.filter(attendees=request.user)
    my_caravans = set([s.caravan for s in my_stops])
    print(my_caravans)
    context = {'all_caravans':all_caravans, 'my_caravans':my_caravans, 'my_stops':my_stops}

    return render(request, 'feed/caravan_list.html', context)

@login_required
def create_caravan(request):
    
    if request.method == 'POST':
        c_form = CaravanCreateForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, f'Your Caravan has been created.')
            c_name = c_form.cleaned_data['name']
            Caravan.objects.filter(name=c_name).first().members.add(request.user)

            #create and save government
            govt = Government.create_standand(c_name)
            govt.save()
            govt.leaders.add(request.user)
            return redirect('update_government', c_name)
    else:
        c_form = CaravanCreateForm(instance=request.user)
    
    #needs to create government as well
    #request.user as government leader

    context = {'c_form':c_form} 
    
    return render(request, 'feed/create_caravan.html', context)

@login_required
def update_government(request, c_name):
    
    c = Caravan.objects.filter(name=c_name).first()
    g = Government.objects.filter(caravan = c).first()

    if request.method == 'POST':
        g_form = GovernmentUpdateForm(request.POST, instance=g)
        if g_form.is_valid():
            g_form.save()
            messages.success(request, f'Your Government has been created.')
            return redirect('caravan', c.name)
        else:
            print(g_form.errors)
    else:
        g_form = GovernmentUpdateForm(instance=g)
    
    #needs to create government as well
    #request.user as government leader

    context = {'g_form':g_form} 
    
    return render(request, 'feed/create_government.html', context)

@login_required
def join_caravan(request, name):
    
    c = Caravan.objects.filter(name=name).first()
    c.members.add(request.user)
    print("Caravan joined")
    
    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def leave_caravan(request, name):
    
    c = Caravan.objects.filter(name=name).first()
    c.members.remove(request.user)
    c_stops = Stop.objects.filter(caravan=c).all()
    for stop in c_stops:
        stop.attendees.remove(request.user)
    print("Left the Caravan")
    
    return HttpResponseRedirect(c.get_absolute_url())


# def search_caravans(request):