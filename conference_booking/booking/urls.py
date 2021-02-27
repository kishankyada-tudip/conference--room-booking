from django.urls import path,include
from rest_framework.routers import DefaultRouter
from booking.views import UserRegisterApi,LoginView,LogoutApi,RoomView,RoomDetailView,SlotView,SlotDetailView,SlotBookView,SlotCancleView

app_name = 'booking'

urlpatterns = [
    path('signup', UserRegisterApi.as_view(), name='signup'),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutApi.as_view(), name="logout"),
    
    path('room', RoomView.as_view(), name="room"),
    path('room/<int:pk>', RoomDetailView.as_view(), name="room"),
    
    path('slot', SlotView.as_view(), name="slot"),
    path('slot/<int:pk>', SlotDetailView.as_view(), name="slot"),
    
    path('slot-book', SlotBookView.as_view(), name="slot-book"),
    path('slot-cancel', SlotCancleView.as_view(), name="slot-cancel")
]