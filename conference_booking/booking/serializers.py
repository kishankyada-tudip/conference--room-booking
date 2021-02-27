from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from booking.models import Room,Slot,User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'is_admin')
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

    def create(self, validated_data):
        user = User(email=validated_data['email'],name=validated_data['name'], is_admin=validated_data['is_admin'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
    
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ("id", "start_time", "end_time", "user", "room", "is_available", "created_date")
    
    def validate(self, data):
        if "start_time" in data and "end_time" in data:
            if data["start_time"] >= data["end_time"]:
                raise serializers.ValidationError({"error": "End time must be greater thanc start time"})
        return super(BookSerializer, self).validate(data)
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields=("id", "name","description", "created_date")