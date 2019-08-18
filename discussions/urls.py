from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.discussion, name='discussion'),
    path('<int:pk>/get_discussion_comments/', views.get_discussion_comments, name='get_discussion_comments'),
    path('<int:pk>/close_discussion/', views.close_discussion, name='close_discussion'),
    path('<int:pk>/remove_discussion/', views.remove_discussion, name='remove_discussion'),
    path('<int:discussion_pk>/remove_discussion_comment/<int:comment_pk>/', views.remove_discussion_comment,
         name='remove_discussion_comment'),
    path('<int:pk>/add_participant/<str:username>/', views.add_participant, name='add_participant'),
    path('<int:pk>/remove_participant/<str:username>/', views.remove_participant, name='remove_participant'),
]
