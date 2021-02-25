from rest_framework import generics, authentication, permissions, status, viewsets
from booking.serializers import UserSerializers, BookSerializer, RoomSerializer
from django.contrib.auth import authenticate,login,logout, get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from booking.models import User,Room,Book
from rest_framework.views import APIView
from django.http import JsonResponse
from datetime import date
    
class UserRegisterApi(generics.CreateAPIView):
    """Use to register the user and automatically it will generate a token for that user."""
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
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LogoutApi(APIView):
    """Use to logout the user"""
    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"success": "Successfully logged out."},status=status.HTTP_200_OK)
 

# Listing, Create, Update, Delete room api Start
class SpecificRoomListingApi(viewsets.ModelViewSet):
    """Retrieve the room detail data based on user authentication if is_admin = True it will return all room else it will return specific room created by employees."""
    serializer_class = RoomSerializer
    queryset = Room.objects.all().order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    

class CreateRoomApis(APIView):
    """Use to create and List new room"""
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        if request.user.is_authenticated:
            caption = request.data.get("caption")
            capacity = request.data.get("capacity")
            user = User.objects.filter(id=request.user.id)
            if user[0].is_admin == True:
                room = Room.objects.create(user=user[0],caption=caption, capacity=capacity)
                return JsonResponse({"id":room.id,
                                     "user":room.user.id,
                                     "caption":room.caption,
                                     "capacity":room.capacity,
                                     "creted_date":room.created_date,
                                     "modified_date":room.modified_date},status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"error":"You are not authorized to book this conference room as you are not an admin."})
  
# Listing, Create, Update, Delete Booking api start
class ConferenceRoomDetailListingApi(viewsets.ModelViewSet):
    """Retrieve the booking detail of conference room data based on user authentication if is_admin = True it will return all booked room else it will return specific room booked by employees."""
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    

class DeleteBookDetailApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """Use to delete booked room if authenticated user is True then it will delete all the  booked room else it won't delete all rooms."""
    def delete(self,request,pk):
        if request.user.is_authenticated:
            book = Book.objects.filter(pk=pk)
            if book:
                book.delete()
                return JsonResponse({"message":"Booked room deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            else:
                return JsonResponse({"message":"Something went wrong!"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": "You are not authorized!"}, status=status.HTTP_401_UNAUTHORIZED) 
            
class UpdateBookDetailApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """use to update the booked room if authenticated user is True then it will update all the  booked room else it won't update all rooms."""
    def put(self,request,pk):
        if request.user.is_authenticated:
            # user = User.objects.filter(id=request.user.id)
            book = Book.objects.filter(pk=pk)
            if book:
                serializer = BookSerializer(book[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    serializer_dict = serializer.data
                    serializer_dict["message"] = "Booked room updated successfully."
                    return Response(serializer_dict)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": "You are not authorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        
class UpdateEmployeeBookDetailApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def put(self,request,pk):
        if request.user.is_authenticated:
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            if start_time >= end_time:
                return JsonResponse({"error": "End time must be greater tha start time"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                booked_room = Book.objects.filter(is_active=True,pk=pk)
                if booked_room:
                    booked_room.update(start_time=start_time,end_time=end_time,is_active=False)
                    return JsonResponse({"message":"Time slot for the booked room updated successfully"},status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({"message":"Room is already reserved"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": "You are not authorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        
    
class BookRoomWithValidationApi(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """Use to check the time slot validation, user validation and create a new conference room"""
    def post(self,request):
        if request.user.is_authenticated:
            room_id = request.data.get("room_id")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")
            users_ids = request.data.get("users_ids")
            # time validation
            if start_time >= end_time:
                return JsonResponse({"error": "End time must be greater tha start time"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                ids = users_ids.split(',')
                my_room = Room.objects.filter(id=room_id)
                if len(ids) != my_room[0].capacity:
                    return JsonResponse({"error": "You are giving users ids more than room capacity."}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    today_date = date.today().strftime("%Y-%m-%d")
                    # user validation
                    ids = users_ids.split(',')
                    user_bookings = Book.objects.filter(start_time__gte=start_time, end_time__lte=end_time)
                    if user_bookings:
                        for i in user_bookings:
                            book_id = i.users_ids.split(',')
                            for b_id in book_id: 
                                for m_id in ids:
                                    if b_id == m_id:
                                        user = User.objects.filter(id=m_id)
                                        return JsonResponse({"error": user[0].name+" is already added in other room"}, status=status.HTTP_401_UNAUTHORIZED)
                                
                    books = Book.objects.filter(created_date=today_date,rooms_id=room_id,start_time__gte=start_time, end_time__lte=end_time)
                    if len(books) != 0:
                        return JsonResponse({"error": "Room is already reserved."}, status=status.HTTP_401_UNAUTHORIZED)                     
                    else:
                        user = User.objects.filter(id=request.user.id)
                        if user[0].is_admin == True:
                            my_room = Room.objects.filter(id=room_id)
                            books = Book.objects.create(user=user[0],rooms=my_room[0],start_time=start_time,end_time=end_time,users_ids=users_ids)
                            if books:
                                return JsonResponse({"id":books.id,
                                                    "user_id":books.user.id,
                                                    "rooms":books.rooms.id,
                                                    "start_time":books.start_time,
                                                    "end_time":books.end_time,
                                                    "is_active":books.is_active,
                                                    "user_ids":books.users_ids,
                                                    "created_date":books.created_date,
                                                    "modified_date":books.modified_date,
                                                    "message": "Room created successfully"}, status=status.HTTP_201_CREATED)
                            else:
                                return JsonResponse({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return JsonResponse({"error": "You are not authorized to book this conference room as you are not an admin"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": "You are not authorized!"}, status=status.HTTP_401_UNAUTHORIZED)    
        
# Listing, Create, Update, Delete Booking api End  
class GetAllUserApi(viewsets.ModelViewSet):
    """Get all users except passed token"""
    serializer_class = UserSerializers
    queryset = User.objects.all().order_by("-id")
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        queryset = self.queryset
        return User.objects.all().exclude(id=self.request.user.id).order_by("-id")