from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from booking.models import Room,Book,User

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
    
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "start_time", "end_time", "user", "rooms", "is_active", "users_ids", "created_date", "modified_date")
    
    def validate(self, data):
        if "start_time" in data and "end_time" in data:
            if data["start_time"] >= data["end_time"]:
                raise serializers.ValidationError({"error": "End time must be greater thanc start time"})
            
        if "users_ids" in data and "rooms"in data:
            ids = data.get('users_ids').split(',')
            my_room = Room.objects.filter(id=data.get('rooms').id)
            if len(ids) != my_room[0].capacity:
                raise serializers.ValidationError({"error": "You are giving users ids more than room capacity."})
                
        if "users_ids" in data and "rooms" in data and "start_time" in data and "end_time" in data:
                ids = data.get('users_ids').split(',')
                user_bookings = Book.objects.filter(start_time__gte=data.get('start_time'), end_time__lte=data.get('end_time'))
                if user_bookings:
                        for i in user_bookings:
                            book_id = i.users_ids.split(',')
                            for b_id in book_id: 
                                for m_id in ids:
                                    if b_id == m_id:
                                        user = User.objects.filter(id=m_id)
                                        raise serializers.ValidationError({"error": user[0].name+" is already added in other room"})
      
        return super(BookSerializer, self).validate(data)
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields=("id", "user", "caption", "capacity", "created_date", "modified_date")
        
        
     