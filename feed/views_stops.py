from .models import *
from .forms import StopCreateForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def stop(request, slug):

    s = Stop.objects.filter(slug=slug).first()
    sf = StopForum.objects.filter(stop=s).first()

    joined = request.user in s.attendees.all()
    caravan_member = request.user in s.caravan.members.all()
    print(caravan_member)

    is_interested = Vote.objects.filter(user=request.user, forum=sf, infavor=True).count() > 0

    context={"s":s, "sf":sf, "joined":joined, 'caravan_member':caravan_member, 'is_interested':is_interested}

    return render(request, 'feed/stop.html', context)

@login_required
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
def add_stop(request, c_name=None):

    context = {}

    if request.method == 'POST':
        s_form = StopCreateForm(request.POST)
        if s_form.is_valid():
         
            # status should be set to proposed and then auto-updated
            # need to create forum

            s = s_form.save()
            messages.success(request, f'Your Stop has been created.')

            sf = StopForum.from_stop(s)
            sf.save()

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

# @login_required
# def edit_stop(request):

#     #must be a leader if decided, or the creator or a leader if tentative or proposal

#     context={}
#     return render(request, 'feed/edit_stop.html', context)

@login_required
def stop_vote_yes(request, slug):

    s = Stop.objects.get(slug=slug)
    u = request.user
    sf = StopForum.objects.get(stop=s)
    v = Vote.create_yes(u,sf)
    v.save()

    return HttpResponseRedirect(f'/feed/stop/{s.slug}')

@login_required
def stop_remove_vote(request, slug):

    s = Stop.objects.get(slug=slug)
    u = request.user
    sf = StopForum.objects.get(stop=s)
    v = Vote.objects.filter(user=u, forum=sf).all()
    v.delete()

    return HttpResponseRedirect(f'/feed/stop/{s.slug}')