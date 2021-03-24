"""travelnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from feed import views as feed_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('feed.urls')),
    path('', user_views.my_profile, name='home'),
    path('users/<slug>/', user_views.profile_view, name='profile_view'),
    path('friends/', user_views.friend_list, name='friend_list'),
    path('users/friend-request/send/<int:id>/', user_views.send_friend_request, name='send_friend_request'), # is this a GET?
    path('users/friend-request/cancel/<int:id>/', user_views.cancel_friend_request, name='cancel_friend_request'),
    path('users/friend-request/accept/<int:id>/', user_views.accept_friend_request, name='accept_friend_request'),
    path('users/friend-request/delete/<int:id>/', user_views.delete_friend_request, name='delete_friend_request'),
    path('users/friend/delete/<int:id>/', user_views.delete_friend, name='delete_friend'),
    path('edit-profile/', user_views.edit_profile, name='edit_profile'),
    path('my-profile/', user_views.my_profile, name='my_profile'),
    path('search_users/', user_views.search_users, name='search_users'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('feed/caravan/<name>/', feed_views.caravan, name='caravan'),
    path('feed/caravan/join/<name>/', feed_views.join_caravan, name='join_caravan'),
    path('feed/caravan/leave/<name>/', feed_views.leave_caravan, name='leave_caravan'),
    path('feed/create-caravan/', feed_views.create_caravan, name='create_caravan'),
    path('feed/update-government/<c_name>', feed_views.update_government, name='update_government'),
    path('feed/caravan-list/', feed_views.caravan_list, name='caravan_list'),
    path('my_stops/', feed_views.my_stops, name='my_stops'),
    path('feed/stop/<slug>/', feed_views.stop, name='stop'),
    path('feed/stop/leave/<slug>', feed_views.leave_stop, name='leave_stop'),
    path('feed/stop/join/<slug>', feed_views.join_stop, name='join_stop'),
    path('feed/add-stop/<c_name>', feed_views.add_stop, name='add_stop'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)