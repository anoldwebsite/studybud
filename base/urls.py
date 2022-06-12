from unicodedata import name
from django.urls import path
# dot means the same directory in which this module is located.
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="home"),  # '' means homepage for app base.
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.retrieve_user_profile, name="user-profile"),
    path('create-room', views.create_room, name="create-room"),
    path('update-room/<str:pk>', views.update_room, name="update-room"),
    path('delete-room/<str:pk>', views.delete_room, name="delete-room"),
    path('delete-message/<str:pk>', views.delete_message, name="delete-message"),
    path('update-user/', views.update_user, name="update-user"),
    path('topics/', views.show_topics_page, name="topics"),
    path('activity/', views.show_activities_page, name="activity")
]
