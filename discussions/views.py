from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from discussions.models import Discussion, Discussion_Comment
from .forms import DiscussionForm, DiscussionCommentForm
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


# load discussion page
def discussion(request, pk):
    d = Discussion.objects.get(pk=pk)
    discussion_comment_form = add_discussion_comment(request, d)
    is_participant = d.participants.all().filter(pk=request.user.pk).exists()
    context = {'user': request.user,
               'discussion': d,
               'is_participant': is_participant,
               'discussion_comment_form': discussion_comment_form
               }
    return render(request, 'discussion.html', context
                  )


# load discussion comments
# called by message_handler.js
def get_discussion_comments(request, pk):
    d = Discussion.objects.get(pk=pk)
    dc = Discussion_Comment.objects.filter(discussion=d, status="open").order_by('-datetime')
    discussion_comment_form = add_discussion_comment(request, d)
    context = {'user': request.user,
               'discussion': d,
               'discussion_comments': dc,
               'discussion_comment_form': discussion_comment_form
               }
    return render(request, 'discussion_comment_section.html', context
                  )


# create a new discussion
# called by user itself from discussion_section in user_profile
def add_discussion(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        discussion_form = DiscussionForm(request.POST or None)
        # check whether it's valid:
        if discussion_form.is_valid():
            # process the data in form.cleaned_data as required
            Discussion.objects.create(owner=page_owner,
                                      title=discussion_form.clean_title(),
                                      message=discussion_form.clean_message())
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        discussion_form = DiscussionForm(None)
    # return render(request, 'registration.html', {'status_form': status_form})
    return discussion_form


# create a new discussion_comment
# called by user itself or visitor from discussion page
def add_discussion_comment(request, d):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        discussion_comment_form = DiscussionCommentForm(request.POST or None)
        # check whether it's valid:
        if discussion_comment_form.is_valid():
            # process the data in form.cleaned_data as required
            Discussion_Comment.objects.create(user=request.user,
                                              discussion=d,
                                              message=discussion_comment_form.clean_discussion_comment())
            # redirect to a new URL:
            discussion_comment_form = DiscussionCommentForm(None)
    # if a GET (or any other method) we'll create a blank form
    else:
        discussion_comment_form = DiscussionCommentForm(None)
    # return render(request, 'registration.html', {'status_form': status_form})
    return discussion_comment_form


# not used
def get_discussion(request, pk):
    d = Discussion.objects.get(pk=pk)
    return d


# close an existing discussion
# called by user itself from discussion_section in user_profile
# closed discussions can be seen, but not edited
def close_discussion(request, pk):
    d = Discussion.objects.get(pk=pk)
    d.status = "closed"
    d.save()
    return HttpResponseRedirect('/user/profile/' + request.user.username + '/')


# remove an existing discussion
# called by user itself or visitor from discussion page
def remove_discussion(request, pk):
    d = Discussion.objects.get(pk=pk)
    d.status = "removed"
    d.save()
    return HttpResponseRedirect('/user/profile/' + request.user.username + '/')


# remove an existing discussion_comment
# called by user itself of discussion_owner from discussion page
def remove_discussion_comment(request, discussion_pk, comment_pk):
    c = Discussion_Comment.objects.get(pk=comment_pk)
    c.status = "removed"
    c.save()
    return HttpResponseRedirect('/discussion/' + str(discussion_pk) + '/')


# add a participant to an existing discussion
# called by user itself from discussion page
def add_participant(request, pk, username):
    d = get_object_or_404(Discussion, pk=pk)
    user = get_object_or_404(User, username=username)
    is_participant = Discussion.objects.filter(Q(pk=pk) & Q(participants__in=[user.pk])).exists()
    if not is_participant:
        d.participants.add(user)
        d.save()
    return HttpResponseRedirect('/discussion/' + str(pk) + '/')


# remove an existing participant from a discussion
# called by user itself from discussion page
def remove_participant(request, pk, username):
    d = Discussion.objects.get(pk=pk)
    user = User.objects.get(username=username)
    # don´t unsubscribe other users
    if request.user.username == username:
        d.participants.remove(user)
        d.save()
    return HttpResponseRedirect('/discussion/' + str(pk) + '/')
