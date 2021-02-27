from django.contrib import admin
from booking.models import User,Slot,Room

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_date", "is_admin", "is_staff"]
    
class SlotAdmin(admin.ModelAdmin):
    list_display = ["id", "created_by","booked_by", "room", "created_date", "start_time", "end_time", "is_available"]
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id","name","description", "created_date"]

admin.site.register(User,UserAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Slot,SlotAdmin)
