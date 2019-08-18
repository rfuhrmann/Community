from django.urls import path
from . import views

urlpatterns = [
    # path('', views.event, name='event'),
    path('<int:pk>/', views.event, name='event'),
    path('<int:pk>/remove_event/', views.remove_event, name='remove_event'),
    # accept / decline / remove invitation from user profile page
    path('<int:pk>/accept_invitation/<str:username>/', views.accept_invitation, name='accept_invitation'),
    path('<int:pk>/decline_invitation/<str:username>/', views.decline_invitation, name='decline_invitation'),
    path('<int:pk>/remove_invitation/<str:username>/', views.remove_invitation, name='remove_invitation'),
    # remove from event page
    path('<int:pk>/remove_participant/<str:username>/', views.remove_participant, name='remove_participant'),
    path('<int:pk>/remove_participation/<str:username>/', views.remove_participation, name='remove_participation'),
    path('no_permissions/<str:uri>/', views.no_permissions, name='no_permissions'),
    path('upcoming/', views.events_upcoming, name='events_upcoming')
]
