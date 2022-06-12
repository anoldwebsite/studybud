from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSrializer
from base.api import serializers


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    # Many object will be serialized e.g., all the chatrooms will be serialized and returned and not just a single room.
    serializers = RoomSrializer(rooms, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSrializer(room, many=False)
    return Response(serializer.data)
