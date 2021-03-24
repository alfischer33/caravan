from django.shortcuts import render, redirect
from .models import Caravan, Stop, Vote, Destination
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django import template


# Create your views here.
def my_stops(request):

    # for s in Stop.objects.all():
    #     s.update_slug()

    my_stops = Stop.objects.filter(attendees=request.user).order_by('start_date')
    stops_by_caravan = {}
    my_caravans = set([s.caravan for s in my_stops])
    #my_caravans = request.user.caravan_set.all()

    for c in my_caravans:
        stops_by_caravan[c] = [my_stops.filter(caravan=c)]
    print(stops_by_caravan)

    context = {'my_stops':my_stops, 'stops_by_caravan':stops_by_caravan}

    return render(request, 'feed/my_stops.html', context)
    
def caravan_list(request):

    all_caravans = Caravan.objects.all()

    my_stops = Stop.objects.filter(attendees=request.user)
    my_caravans = set([s.caravan for s in my_stops])
    print(my_caravans)
    context = {'all_caravans':all_caravans, 'my_caravans':my_caravans, 'my_stops':my_stops}

    return render(request, 'feed/caravan_list.html', context)

def caravan(request, name):

    u = request.user
    c = Caravan.objects.filter(name=name).first()
    ismember = request.user in c.members.all()
    stops = Stop.objects.filter(caravan=c).all()

    #https://www.abidibo.net/blog/2014/05/22/check-if-user-belongs-group-django-templates/
    # register = template.Library()
    # @register.filter(name='attending_stop')
    # def attending_stop(u, s):
    #     return (u in s.attendees.all())

    context={"c":c, "ismember":ismember, "stops":stops}
    

    return render(request, 'feed/caravan.html', context)

def stop(request, slug):

    s = Stop.objects.filter(slug=slug).first()
    print(s)

    joined = request.user in s.attendees.all()
    caravan_member = request.user in s.caravan.members.all()
    print(caravan_member)

    context={"s":s, "joined":joined, 'caravan_member':caravan_member}

    return render(request, 'feed/stop.html', context)

@login_required
def join_stop(request, slug):
    
    s = Stop.objects.filter(slug=slug).first()

    if request.user in s.caravan.members.all():
        s.attendees.add(request.user)
        print("Stop joined")
    else:
        print("ERROR: You must join this caravan first")
    
    return HttpResponseRedirect(f'/feed/stop/{s.slug}')

@login_required
def leave_stop(request, slug):
    
    s = Stop.objects.filter(slug=slug).first()
    s.attendees.remove(request.user)
    print("Stop removed")
    
    return HttpResponseRedirect(f'/feed/stop/{s.slug}')

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

@login_required
def add_stop(request, c_name=None):

    context = {}

    if request.method == 'POST':
        s_form = StopCreateForm(request.POST)
        if s_form.is_valid():
            
            # status should be set to proposed and then auto-updated
            # need to create forum

            s_form.save()
            messages.success(request, f'Your Stop has been created.')
            return redirect('caravan', c_name)
    else:
        # if c_name == None:
        #     sc_form = StopCaravanForm(instance=request.user)
        #     context = {'sc_form':sc_form}
        #     render(request, 'feed/add_stop_caravan.html', context)
        # elif len(Caravan.objects.filter(name=c_name).all()) == 1:
        #     s_form = StopCreateForm(instance=request.user)
        #     context = {'s_form':s_form, 'c_name': c_name}
        #     return render(request, 'feed/add_stop.html', context)
        # else:
        #     print('caravan_name not valid')
        #     pass

        s_form = StopCreateForm(instance=request.user)
        context = {'s_form':s_form, 'c_name': c_name}
        return render(request, 'feed/add_stop.html', context)
    #context={}
    #return render(request, 'feed/add_stop.html', context)


def edit_stop(request):

    #must be a leader if decided, or the creator or a leader if tentative or proposal

    context={}
    return render(request, 'feed/edit_stop.html', context)

# def search_stops(request):
# def search_caravans(request):