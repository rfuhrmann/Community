from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()
from users.models import Privacy


# load welcome page
def welcome(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            # log in the user
            current_user = authenticate(username=login_form.clean_username(), password=login_form.clean_password())
            if current_user is not None:
                login(request, current_user)
                return HttpResponseRedirect('/user/profile/' + current_user.username + '/')
    else:
        login_form = LoginForm()
    return render(request, 'welcome.html', {'login_form': login_form})


# load signup page
def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        signup_form = SignupForm(request.POST or None)
        # check whether it's valid:
        if signup_form.is_valid():
            # process the data in form.cleaned_data as required
            current_user = User.objects.create_user(username=signup_form.clean_username(),
                                                    password=signup_form.clean_password(),
                                                    first_name=signup_form.clean_first_name(),
                                                    last_name=signup_form.clean_last_name(),
                                                    email=signup_form.clean_email(),
                                                    phone=signup_form.clean_phone())
            test = authenticate(request, username=current_user.username, password=signup_form.clean_password())
            Privacy.objects.create(user=current_user)
            if test is not None:
                login(request, current_user)
            # redirect to a new URL:
            return HttpResponseRedirect('/user/profile/' + current_user.username + '/')
    else:
        signup_form = SignupForm()
    context = {'user': request.user,
               'signup_form': signup_form}
    return render(request, 'registration.html', context)
