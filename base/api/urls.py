from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    # http://127.0.0.1:8000/api/rooms/25
    path('rooms/<str:pk>', views.get_room)
]
