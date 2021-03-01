from rest_framework import generics, authentication, permissions, status, viewsets
from booking.serializers import UserSerializers, SlotSerializer, RoomSerializer
from django.contrib.auth import authenticate,login,logout, get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from booking.models import User,Room,Slot
from rest_framework.views import APIView
from django.http import JsonResponse
from datetime import date
    
class UserRegisterApi(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializers

class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"message": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutApi(APIView):
    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"success": "Successfully logged out."},status=status.HTTP_200_OK)
    
class RoomView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        if request.user.is_authenticated:
            name = request.data.get("name")
            description = request.data.get("description")
            if request.user.is_admin == True:
                room = Room.objects.create(name=name, description=description)
                return JsonResponse({"id":room.id,
                                     "name":room.name,
                                     "description":room.description,
                                     "messsage":"room created successfully"},status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"message":"you are not authorize to create this room."})
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
                    
    def get(self,request):
        if request.user.is_authenticated:
            data = []
            search_room =  self.request.query_params.get("search_room")
            if search_room:
                room = Room.objects.filter(name__icontains=search_room)
                for i in room:
                    response = {"id":i.id,
                                "name":i.name,
                                "description":i.description,
                                "created_date":i.created_date}
                    data.append(response)
                return JsonResponse(data, safe=False)
            else:
                room = Room.objects.all().order_by("-id")
                for i in room:
                    response = {"id":i.id,
                                "name":i.name,
                                "description":i.description,
                                "created_date":i.created_date}
                    data.append(response)
                return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
        
class RoomDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,pk):
        if request.user.is_authenticated:
            data = []
            room = Room.objects.filter(pk=pk)
            if room:
                response = {"id":room[0].id,
                            "name":room[0].name,
                            "description":room[0].description,
                            "created_date":room[0].created_date}
                data.append(response)
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({"message":"room does not exist"})
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
        
    def delete(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_admin == True:
                room = Room.objects.filter(pk=pk)
                if room:
                    room.delete()
                    return JsonResponse({"message":"Room deleted successfully"}, status= status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({"message":"Room does not exist."})
            else:
                return JsonResponse({"message":"You are not authorized to delete this room."},status = status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
        
    def put(self,request,pk):
        if request.user.is_authenticated:
            name = request.data.get("name")
            description = request.data.get("description")
            if request.user.is_admin == True:
                room = Room.objects.filter(pk=pk)
                if room:
                    room.update(name=name, description=description)
                    return JsonResponse({"id":room[0].id,
                                        "name":room[0].name,
                                        "description":room[0].description,
                                        "message":"room updated successfully"})
                else:
                    return JsonResponse({"message":"room does not exist"})
            else:
                return JsonResponse({"message":"You are not authorized to update this room."},status = status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
        
class SlotView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        if request.user.is_authenticated:
            room_id = request.data.get("room_id")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            
            if request.user.is_admin == True:
                if start_time >= end_time:
                    return JsonResponse({"message":"End time should not be less than start time."})
                else:
                    today_date = date.today().strftime("%Y-%m-%d")
                    slot = Slot.objects.filter(created_date=today_date,room_id=room_id,start_time__lte=start_time, end_time__gte=end_time)
                    if len(slot) != 0:
                        return JsonResponse({"message": "Time slot overlapping for the room"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user = User.objects.filter(id=request.user.id)
                        if user[0]:
                            my_room = Room.objects.filter(id=room_id)
                            slots = Slot.objects.create(created_by=user[0],room=my_room[0],start_time=start_time,end_time=end_time)
                            if slots:
                                return JsonResponse({"id":slots.id,
                                                     "user_id":slots.created_by.id,
                                                     "room_id":slots.room.id,
                                                     "start_time":slots.start_time,
                                                     "end_time":slots.end_time,
                                                     "is_available":slots.is_available,
                                                     "message":"room booked successfully"},status=status.HTTP_201_CREATED)
                            else:
                                return JsonResponse({"message":"Slot does not exist."})
                        else:
                            return JsonResponse({"message":"you don't have permission to book this room"})
            else:
                return JsonResponse({"message":"Employee can't create this slot"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self,request):
        if request.user.is_authenticated:
            room_id = self.request.query_params.get("room_id")
            is_available = self.request.query_params.get("is_available")
            data = []
            if room_id or is_available:
                slot = Slot.objects.filter(room_id=room_id,is_available=is_available).order_by("-id")
                if slot:
                    for i in slot:
                        response = {"id":i.id,
                                    "user_id":i.created_by.id,
                                    "room_id":i.room.id,
                                    "start_time":i.start_time,
                                    "end_time":i.end_time,
                                    "is_available":i.is_available}
                        data.append(response)
                    return JsonResponse(data, safe=False)
                else:
                    return JsonResponse({"message":"No slots available."})
            else:
                slot = Slot.objects.all().order_by("-id")
                for i in slot:
                    response = {"id":i.id,
                                "user_id":i.created_by.id,
                                "room_id":i.room.id,
                                "start_time":i.start_time,
                                "end_time":i.end_time,
                                "is_available":i.is_available}
                    data.append(response)
                return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED)
        
class SlotDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,pk):
        if request.user.is_authenticated:
            slot = Slot.objects.filter(pk=pk)
            if slot:
                return JsonResponse({"id":slot[0].id,
                                    "user_id":slot[0].created_by.id,
                                    "room_id":slot[0].room.id,
                                    "start_time":slot[0].start_time,
                                    "end_time":slot[0].end_time,
                                    "is_available":slot[0].is_available})
            else:
                return JsonResponse({"message":"No slots available"})
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self,request,pk):
        if request.user.is_authenticated:
            if request.user.is_admin == True:
                slot = Slot.objects.get(pk=pk)
                if slot:
                    slot.delete()
                    return JsonResponse({"message":"Slot deleted successfully"}, status= status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({"message":"Slot does not exist."})
            else:
                return JsonResponse({"message":"Employee can't delete this slot."},status = status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message":"You are not authorize!"}, status= status.HTTP_401_UNAUTHORIZED)
        
    def put(self,request,pk):
        if request.user.is_authenticated:
            room_id = request.data.get("room_id")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            if request.user.is_admin == True:
                if start_time >= end_time:
                    return JsonResponse({"message":"start time cannot be greater then end time"})
                else:
                    today_date = date.today().strftime("%Y-%m-%d")
                    slots = Slot.objects.filter(pk=pk,created_date=today_date,room_id=room_id,start_time__lte=start_time, end_time__gte=end_time)
                    if len(slots) != 0:
                        return JsonResponse({"message": "Time slot overlapping for the room"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user = User.objects.filter(id=request.user.id)
                        if user[0]:
                            my_room = Room.objects.filter(id=room_id)
                            slots = Slot.objects.filter(pk=pk)
                            if slots:
                                slots.update(room=my_room[0],start_time=start_time,end_time=end_time,created_date=today_date)
                                return JsonResponse({"id":slots[0].id,
                                                     "user_id":slots[0].created_by.id,
                                                     "room_id":slots[0].room.id,
                                                     "start_time":slots[0].start_time,
                                                     "end_time":slots[0].end_time,
                                                     "is_available":slots[0].is_available,
                                                     "message":"slot updated successfully"},status=status.HTTP_201_CREATED)
                            else:
                                return JsonResponse({"message":"Slot does not exist."})
                        else:
                            return JsonResponse({"message":"you don't have permission to book this room"})
            else:
                return JsonResponse({"message":"Employee can't update this slots"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED)
        
        
class SlotBookView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        if request.user.is_authenticated:
            room_id = request.data.get("room_id")
            slot_id = request.data.get("slot_id")
            if request.user.is_admin == False:
                slot = Slot.objects.filter(id=slot_id, room_id=room_id, is_available=True)
                if slot:
                    slot.update(is_available=False,booked_by=request.user.id)
                    return JsonResponse({"message":"slot booked successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({"message":"Slot does not exist"})
            else:
                return JsonResponse({"message":"Admin can't book a slot"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED)
        
class SlotCancleView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        if request.user.is_authenticated:
            room_id = request.data.get("room_id")
            slot_id = request.data.get("slot_id")
            if request.user.is_admin == False:
                slot = Slot.objects.filter(id=slot_id, room_id=room_id, is_available=False)
                if slot:
                    slot.update(is_available=True,booked_by=None)
                    return JsonResponse({"message":"slot booked cancelled successfully"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({"message":"Slot does not exist."})
            else:
                return JsonResponse({"message":"Admin can't unbooke a slot"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"message":"you are not authorized!!!"},status=status.HTTP_401_UNAUTHORIZED) 