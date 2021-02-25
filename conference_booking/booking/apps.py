from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'booking'
    
    def ready(self):
        from booking import updater
        updater.start()
