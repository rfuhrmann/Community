from users.models import Address, User, Friendship, Status, Status_Comment, Privacy
from django.http import HttpResponse, HttpResponseRedirect
from .forms import StatusForm, StatusCommentForm, UserForm, ContactForm, PasswordForm, AddressForm, FriendForm, \
    PrivacyForm, ImageForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout


# add a new status to user_profile
# called by user itself from user_profile
def add_status(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        status_form = StatusForm(request.POST or None)

        # check whether it's valid:
        if status_form.is_valid():
            # process the data in form.cleaned_data as required
            Status.objects.create(owner=page_owner,
                                  title=status_form.clean_title(),
                                  message=status_form.clean_message())
            # redirect to a new URL:
            return HttpResponseRedirect('')
    # if a GET (or any other method) we'll create a blank form
    else:
        status_form = StatusForm(None)
    # return render(request, 'registration.html', {'status_form': status_form})
    return status_form


# add a new comment to an existing status in user_profile
# called by a visitor from user_profile
def add_status_comment(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        status_comment_form = StatusCommentForm(request.POST or None)
        # check whether it's valid:
        if status_comment_form.is_valid():
            # process the data in form.cleaned_data as required
            status = page_owner.status.all().order_by('-datetime').first()
            s = Status_Comment.objects.create(user=request.user,
                                              status=status,
                                              message=status_comment_form.clean_comment_message())
            # redirect to a new URL:
            return HttpResponseRedirect('')
    # if a GET (or any other method) we'll create a blank form
    else:
        status_comment_form = StatusCommentForm(None)
    # return render(request, 'registration.html', {'status_form': status_form})
    return status_comment_form


# add a new user
# called by user itself from welcome page
def add_user(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_form = UserForm(request.POST or None)
        # check whether it's valid:
        if user_form.is_valid():
            # process the data in form.cleaned_data as required
            # do not update username or email
            if user_form.clean_password() != "":
                user = page_owner
                user.password = user_form.clean_password()
                update_session_auth_hash(request, user)
            # if user_form.clean_password() != "":
            #     request.user.password = user_form.clean_password()
            page_owner.first_name = user_form.clean_first_name()
            page_owner.last_name = user_form.clean_last_name()
            page_owner.phone = user_form.clean_phone()
            page_owner.save()
            # redirect to a new URL:
        # if a GET (or any other method) we'll create a blank form
    else:
        # set default values from user model
        user_form = UserForm(initial={'username': page_owner.username,
                                      'first_name': page_owner.first_name,
                                      'last_name': page_owner.last_name,
                                      'email': page_owner.email,
                                      'phone': page_owner.phone})
    return user_form


# add a new contact to user_profile
# called by user itself from user_profile
def add_contact(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        contact_form = ContactForm(request.POST or None)
        # check whether it's valid:
        if contact_form.is_valid():
            # process the data in form.cleaned_data as required
            page_owner.first_name = contact_form.clean_first_name()
            page_owner.last_name = contact_form.clean_last_name()
            page_owner.phone = contact_form.clean_phone()
            page_owner.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        contact_form = ContactForm(initial={'first_name': page_owner.first_name,
                                            'last_name': page_owner.last_name,
                                            'email': page_owner.email,
                                            'phone': page_owner.phone})
    return contact_form


# add a new password to user_profile
# called by user itself from user_profile
def add_password(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        password_form = PasswordForm(request.POST or None)
        # check whether it's valid:
        if password_form.is_valid():
            # logout
            logout(request)
            # save new password
            page_owner.set_password(password_form.clean_password())
            page_owner.save()
            # login
            test = authenticate(request, username=page_owner.username, password=password_form.clean_password())
            if test is not None:
                login(request, page_owner)
    # if a GET (or any other method) we'll create a blank form
    else:
        password_form = PasswordForm()
    return password_form


# add a new address to user_profile
# called by user itself from user_profile
def add_address(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        address_form = AddressForm(request.POST or None)
        # check whether it's valid:
        if address_form.is_valid():
            # process the data in form.cleaned_data as required
            address, created = Address.objects.get_or_create(country=address_form.clean_country(),
                                                             postal_code=address_form.clean_postal_code(),
                                                             town=address_form.clean_town(),
                                                             street=address_form.clean_street(),
                                                             street_number=address_form.clean_street_number())
            page_owner.address = address
            page_owner.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        if page_owner.address:
            address_form = AddressForm(initial={'country': page_owner.address.country,
                                                'postal_code': page_owner.address.postal_code,
                                                'town': page_owner.address.town,
                                                'street': page_owner.address.street,
                                                'street_number': page_owner.address.street_number})
        else:
            address_form = AddressForm(None)
    return address_form


# add a new friendship request to user_profile
# called by user itself from user_profile
def add_friend(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        friend_form = FriendForm(request.POST or None)
        # check whether it's valid:
        if friend_form.is_valid():
            # process the data in form.cleaned_data as required
            recipient = User.objects.get(username=request.POST.get('username', False))
            # recipient = User.objects.get(username=request.POST['username'])
            Friendship.objects.get_or_create(sender=page_owner,
                                             recipient=recipient,
                                             status="request"
                                             )
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        friend_form = FriendForm(initial={'current_username': page_owner.username})
        # friend_form = FriendForm(initial={'current_username': request.POST['username']})
    # return render(request, 'registration.html', {'status_form': status_form})
    return friend_form


# add new privacy settings to user_profile
# called by user itself from user_profile
def add_privacy(request, page_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        privacy_form = PrivacyForm(request.POST or None)
        # check whether it's valid:
        if privacy_form.is_valid():
            # process the data in form.cleaned_data as required
            page_owner.privacy.contact = privacy_form.clean_contact()
            page_owner.privacy.address = privacy_form.clean_address()
            page_owner.privacy.status_comments = privacy_form.clean_status_comments()
            page_owner.privacy.friends = privacy_form.clean_friends()
            page_owner.privacy.discussions = privacy_form.clean_discussions()
            page_owner.privacy.events = privacy_form.clean_events()
            page_owner.privacy.groups = privacy_form.clean_groups()
            page_owner.privacy.save()
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        # set default values from user model
        privacy_form = PrivacyForm(initial={'contact': page_owner.privacy.contact,
                                            'address': page_owner.privacy.address,
                                            'status_comments': page_owner.privacy.status_comments,
                                            'friends': page_owner.privacy.friends,
                                            'discussions': page_owner.privacy.discussions,
                                            'events': page_owner.privacy.events,
                                            'groups': page_owner.privacy.groups})
    return privacy_form
