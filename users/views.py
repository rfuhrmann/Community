from django.shortcuts import render, get_object_or_404
from users.models import Address, User, Friendship, Status, Status_Comment, Privacy
from discussions.models import Discussion
from events.models import Event, EventInvitation
from django.http import HttpResponse, HttpResponseRedirect
from .forms import StatusForm, StatusCommentForm, ImageForm
from discussions.views import add_discussion
from events.views import add_event
# add build_functions for forms
from .build_forms import add_status, add_status_comment, add_contact, add_password, add_address, add_friend, \
    add_privacy, add_user
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()
import datetime


# Create your views here.

# loads user_profile page
def user_profile(request, username):
    page_owner = get_object_or_404(User, username=username)

    # loading forms
    status_form = add_status(request, page_owner)
    status_comment_form = add_status_comment(request, page_owner)
    contact_form = add_contact(request, page_owner)
    address_form = add_address(request, page_owner)
    password_form = add_password(request, page_owner)
    friend_form = add_friend(request, page_owner)
    privacy_form = add_privacy(request, page_owner)
    user_form = add_user(request, page_owner)
    discussion_form = add_discussion(request, page_owner)
    event_form = add_event(request, page_owner)
    profile_image_form = add_profile_image(request)

    # loading data from db
    status = page_owner.status.all().order_by('-datetime')
    discussions = Discussion.objects.filter(Q(participants__in=[page_owner.pk]) | Q(owner=page_owner) & ~Q(status='removed')).distinct()
    events = Event.objects.filter(Q(participants__in=[page_owner.pk]) & Q(status='open')).distinct()
    event_invitations = EventInvitation.objects.filter(Q(recipient=page_owner) & Q(status='request')).distinct()
    friendships = Friendship.objects.filter(Q(status='accepted') & (Q(sender=page_owner) | Q(recipient=page_owner)))
    f_receipt = page_owner.friendships_receipt.filter(status='request')
    f_requested = page_owner.friendships_requested.filter(Q(status='request') | Q(status="declined"))
    if not request.user.is_authenticated:
        user_is_a_friend = False
    else:
        user_is_a_friend = Friendship.objects.filter(
            Q(status='accepted') & (Q(sender=request.user) | Q(recipient=request.user))).exists()

    # prepare data if empty
    if request.user == page_owner:
        user_is_a_friend = False
    # check if content is existing in db
    if status.count() < 1:
        status = None
    if f_receipt.count() < 1:
        f_receipt = None
    if f_requested.count() < 1:
        f_requested = None
    if friendships.count() < 1:
        friendships = None
    if page_owner.address is not None:
        address = page_owner.address
    else:
        address = None
    if discussions.count() < 1:
        discussions = None
    if events.count() < 1:
        events = None
    if event_invitations.count() < 1:
        event_invitations = None

    # set context
    context = {'user': request.user,
               'page_owner': page_owner,
               'user_is_a_friend': user_is_a_friend,
               'status': status,
               'address': address,
               'friendships': friendships,
               'friendships_receipt': f_receipt,
               'friendships_requested': f_requested,
               'privacy': page_owner.privacy,
               'discussions': discussions,
               'events': events,
               'event_invitations': event_invitations,
               'status_form': status_form,
               'status_comment_form': status_comment_form,
               'user_form': user_form,
               'contact_form': contact_form,
               'password_form': password_form,
               'address_form': address_form,
               'friend_form': friend_form,
               'privacy_form': privacy_form,
               'discussion_form': discussion_form,
               'event_form': event_form,
               'profile_image_form': profile_image_form}
    return render(request, 'user_profile.html', context)


# mark a user as not active
# called by user itself from user_profile
def remove_user(request, username):
    request.user.is_active = False
    request.user.save()
    return HttpResponseRedirect('/base/logout/')


# accept a friendship request
# called by user itself from friendship_section
def accept_friendship(request, username, pk):
    f = Friendship.objects.get(pk=pk)
    f.status = "accepted"
    f.response_datetime = datetime.datetime.now()
    f.save()
    u = User.objects.get(username=username)
    friend = User.objects.get(username=f.sender.username)
    u.friends.add(friend)
    u.save()
    friend.friends.add(u)
    friend.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# decline a friendship request
# called by user itself from user_profile
def decline_friendship(request, username, pk):
    f = Friendship.objects.get(pk=pk)
    f.status = "declined"
    f.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# remove an existing friendship
# called by one user of the friendship from friendship_section
def remove_friendship(request, username, pk):
    f = Friendship.objects.get(pk=pk)
    f.status = "removed"
    f.save()
    u = User.objects.get(username=username)
    if f.sender.username == username:
        friend = User.objects.get(username=f.recipient.username)
    else:
        friend = User.objects.get(username=f.sender.username)
    u.friends.remove(friend)
    u.save()
    friend.friends.remove(u)
    friend.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# upload a new profile image
# not implemented
def add_profile_image(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        profile_image_form = ImageForm(request.POST or None)
        # check whether it's valid:
        if profile_image_form.is_valid():
            # process the data in form.cleaned_data as required
            request.user.img = profile_image_form.clean_img()
            request.user.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        # set default values from user model
        profile_image_form = ImageForm()
    return profile_image_form
