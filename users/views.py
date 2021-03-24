from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, FriendRequest
from django.contrib.auth import get_user_model
#from feed.models import Post
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.conf import settings

User = get_user_model()

# Create your views here.
def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {'friends':friends}
    return render(request,"users/friend_list.html", context)

@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user
    )
    return HttpResponseRedirect(f'/users/{user.profile.slug}')

@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect(f'/users/{user.profile.slug}')

@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=from_user,
        to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect(f'/users/{request.user.profile.slug}')

@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect(f'/users/{request.user.profile.slug}')

def delete_friend(request, id):
    user_profile = request.user.profile
    friend_profile = get_object_or_404(User, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return HttpResponseRedirect(f'/users/{friend_profile.slug}')

def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user) # think this should just be u
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    #user_posts = Post.objects.filter(user_name=u) # u.username?

    friends = p.friends.all()

    # check friend status
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        if len(FriendRequest.objects.filter(from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u':u,
        'button_status':button_status,
        'friends_list':friends,
        'sent_friend_requests':sent_friend_requests,
        #'post_count': user_posts.count,
        'rec_friend_requests':rec_friend_requests
    }

    return render(request, 'users/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('my_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {'u_form':u_form, 'p_form':p_form} 
    return render(request, 'users/edit_profile.html', context)

@login_required
def my_profile(request):
    p = request.user.profile
    me = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=me)
    rec_friend_requests = FriendRequest.objects.filter(to_user=me)
    #user_posts = Post.objects.filter(user_name=you)
    friends = p.friends.all()
    button_status = 'none'
	
    context = {
        'u':me,
        'button_status':button_status,
        'friends_list':friends,
        'sent_friend_requests':sent_friend_requests,
        #'post_count':user_posts.count,
        'rec_friend_requests':rec_friend_requests
    }

    return render(request,"users/profile.html",context)

@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {'users':object_list}
    return render(request, "users/search_users.html",context)