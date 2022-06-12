# serializers.py will take python objects, serialize them and give us a JSON object.
from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSrializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
