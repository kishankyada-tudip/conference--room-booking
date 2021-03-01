from booking.models import Slot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import csv

now = datetime.now().time()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(TimeSlots, 'interval', seconds=1)
    scheduler.start()

def TimeSlots():
    slot = Slot.objects.filter(is_available=False,booked_by__isnull=False)
    for i in slot:
        if i.end_time <= now:
            i.is_available = True
            i.booked_by = None
            i.save()
            with open("conference_booking_slot.csv", mode='w') as f:
                fieldnames = ['Room name', 'Start time', 'End time']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({"Room name":i.room.name, "Start time":i.start_time, "End time":i.end_time})