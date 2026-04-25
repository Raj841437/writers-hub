from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),  # IMPORTANT
]
path('send-request/<str:username>/', views.send_request, name='send_request'),
path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
path('chat/<str:username>/', views.chat, name='chat'),