
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from booking.views import UserRegisterApi,LoginView,\
                          ConferenceRoomDetailListingApi,LogoutApi,\
                          BookRoomWithValidationApi,CreateRoomApis,SpecificRoomListingApi,\
                          GetAllUserApi,DeleteBookDetailApi,UpdateBookDetailApi,UpdateEmployeeBookDetailApi



router = DefaultRouter()
router.register('conference-room-detail-listing', ConferenceRoomDetailListingApi)
router.register('specific-rooms-listing', SpecificRoomListingApi)
router.register('user-list', GetAllUserApi)
# router.register('create-room-api', CreateRoomApi)

app_name = 'booking'

urlpatterns = [
    
    path('', include(router.urls)),
    
    path('signup', UserRegisterApi.as_view(), name='signup'),
    path('login', LoginView.as_view(), name="login"),
    path('logout',LogoutApi.as_view(), name="logout"),
    
    path('create-room-api',CreateRoomApis.as_view(),name="create-room-api"),
    
    path('admin-book-rooms',BookRoomWithValidationApi.as_view(), name="book-rooms"),
    # path('update-room/<int:pk>',UpdateRoomApi.as_view(), name="update-room"),
    # path('delete-room/<int:pk>',DeleteRoomApi.as_view(), name="delete-room"),
    
    path('delete-booked-room/<int:pk>',DeleteBookDetailApi.as_view(), name="delete-booked-room"),
    path('update-booked-room/<int:pk>',UpdateBookDetailApi.as_view(), name="update-booked-room"),
    
    path('employee-update-room/<int:pk>',UpdateEmployeeBookDetailApi.as_view(), name="employee-update-room"),
]