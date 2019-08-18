from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
# Create your views here.


# logout user and redirect to startpage
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')
