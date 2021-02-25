from django.contrib import admin
from booking.models import User,Book,Room

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_date", "modified_date", "is_admin", "is_staff"]
    
class BooksAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "rooms", "created_date", "modified_date", "start_time", "end_time", "users_ids", "is_active"]
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "user","caption","capacity", "created_date", "modified_date"]

admin.site.register(User,UserAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Book,BooksAdmin)
