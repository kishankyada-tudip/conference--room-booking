from booking.models import Book
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

now = datetime.now().time()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(TimeSlots, 'interval', minutes=1)
    scheduler.start()

def TimeSlots():
    book = Book.objects.filter(is_active=False)
    for i in book:
        if i.end_time < now:
            i.is_active = True
            i.save()
            


            
    