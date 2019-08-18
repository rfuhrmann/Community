from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EventForm, ParticipantForm
from events.models import Event, EventInvitation, Place
from users.models import Address
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()
import datetime


# load event page
def event(request, pk):
    curr_event = Event.objects.get(pk=pk)
    event_owner = curr_event.owner
    curr_user = request.user
    is_participant = curr_event.participants.all().filter(pk=curr_user.pk).exists()
    # no permissions => redirect to warning page
    if curr_user != event_owner and not is_participant:
        uri = request.build_absolute_uri()
        uri = uri.replace('/', '_')
        return HttpResponseRedirect('/event/no_permissions/' + uri + '/')
    # set place to None (hide) if no place.name
    if curr_event.place:
        if not curr_event.place.name:
            curr_event.place = None
    # process event_form
    # fill with initial values
    # update curr_event, in case changes have been applied
    event_form = edit_event(request, curr_event)
    curr_event = Event.objects.get(pk=pk)
    participant_form = add_participant(request, curr_event)
    participants = curr_event.participants.all()
    context = {'page_owner': event_owner,
               'user': curr_user,
               'event': curr_event,
               'is_participant': is_participant,
               'participants': participants,
               'event_form': event_form,
               'participant_form': participant_form}
    return render(request, 'event.html', context)


# load upcoming_events page
def events_upcoming(request):
    events = Event.objects.filter(end_datetime__gte=datetime.datetime.now())
    context = {'events': events}
    return render(request, 'upcoming_events.html', context)


# add a new event to db
# called by user itself from user_profile
def add_event(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        event_form = EventForm(request.POST or None)
        # check whether it's valid:
        if event_form.is_valid():
            place, created = Place.objects.get_or_create(name=event_form.clean_place_name(),
                                                         description=event_form.clean_place_description())
            # create event
            curr_event = Event.objects.create(owner=request.user,
                                              name=event_form.clean_name(),
                                              description=event_form.clean_description(),
                                              category=event_form.clean_category(),
                                              start_datetime=event_form.clean_start_datetime(),
                                              end_datetime=event_form.clean_end_datetime(),
                                              place=place)

            curr_event.participants.add(page_owner)
            curr_event.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        event_form = EventForm(None)
    return event_form


# edit an existing event
# called by user itself from event page
def edit_event(request, curr_event):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        event_form = EventForm(request.POST or None)
        # check whether it's valid:
        if event_form.is_valid():
            # edit place
            place, created = Place.objects.get_or_create(name=event_form.clean_place_name(),
                                                         description=event_form.clean_place_description())
            # edit event
            curr_event = Event.objects.get(pk=curr_event.pk)
            curr_event.name = event_form.clean_name()
            curr_event.description = event_form.clean_description()
            curr_event.category = event_form.clean_category()
            curr_event.start_datetime = event_form.clean_start_datetime()
            curr_event.end_datetime = event_form.clean_end_datetime()
            curr_event.place = place
            curr_event.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        event_form = EventForm(initial={'name': curr_event.name,
                                        'description': curr_event.description,
                                        'category': curr_event.category,
                                        'start_datetime': curr_event.start_datetime,
                                        'end_datetime': curr_event.end_datetime,
                                        'place_name': curr_event.place.name,
                                        'place_description': curr_event.place.description})
    return event_form


# add a new participant to an existing event
# called by user itself from event page
def add_participant(request, curr_event):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        participant_form = ParticipantForm(request.POST or None)
        # check whether it's valid:
        if participant_form.is_valid():
            # process the data in form.cleaned_data as required
            participant = User.objects.get(username=request.POST.get('username', False))
            EventInvitation.objects.get_or_create(event=curr_event,
                                                  sender=request.user,
                                                  recipient=participant,
                                                  status="request")
            # redirect to a new URL:
        # if a GET (or any other method) we'll create a blank form
    else:
        participant_form = ParticipantForm(initial={'current_username': request.user.username,
                                                    'event_id': curr_event.pk})
    return participant_form


# remove a participant from an event
# called by event_owner from event page
def remove_participant(request, pk, username):
    e = Event.objects.get(pk=pk)
    user = get_object_or_404(User, username=username)
    # page_owner cannot remove himself
    if e.owner == user:
        return HttpResponseRedirect('/event/' + str(pk) + '/')
    e.participants.remove(user)
    e.save()
    return HttpResponseRedirect('/event/' + str(pk) + '/')


# remove a participant from an event
# called by user itself from event_section in user_profile
def remove_participation(request, pk, username):
    e = Event.objects.get(pk=pk)
    user = get_object_or_404(User, username=username)
    # page_owner cannot remove himself
    if e.owner == user:
        return HttpResponseRedirect('/event/' + str(pk) + '/')
    e.participants.remove(user)
    e.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# accept an event_invitation
# called by user itself from event_section in user_profile
def accept_invitation(request, pk, username):
    u = User.objects.get(username=username)
    ei = EventInvitation.objects.get(pk=pk)
    if ei:
        # accept invitation
        ei.status = "accepted"
        ei.save()
        # add user to participants
        ei.event.participants.add(u)
        ei.event.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# decline an event_invitation
# called by user itself from event_section in user_profile
def decline_invitation(request, pk, username):
    ei = EventInvitation.objects.get(pk=pk)
    if ei:
        ei.status = "declined"
        ei.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# remove an existing event_invitation (participation)
# called by event_owner from event page
def remove_invitation(request, pk, username):
    ei = EventInvitation.objects.get(pk=pk)
    if ei:
        ei.status = "removed"
        ei.save()
    return HttpResponseRedirect('/user/profile/' + username + '/')


# remove an existing event
# called by event_owner from event_section in user_profile
def remove_event(request, pk):
    curr_event = Event.objects.get(pk=pk)
    for i in curr_event.invitations.all():
        i.status = "removed"
        i.save()
    curr_event.status = "removed"
    curr_event.save()
    return HttpResponseRedirect('/user/profile/' + request.user.username + '/')


# show warning page if user has no permission to see an event
# that´s the case if user is no participant
def no_permissions(request, uri):
    message = "You have no permissions to access this page"
    context = {'message': message,
               'uri': uri}
    return render(request, 'warning_no_permissions.html', context)
