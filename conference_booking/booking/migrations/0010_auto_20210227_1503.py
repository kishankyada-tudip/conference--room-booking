# Generated by Django 3.0 on 2021-02-27 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20210226_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='user',
        ),
        migrations.AddField(
            model_name='slot',
            name='booked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked_slots', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='slot',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_slots', to=settings.AUTH_USER_MODEL),
        ),
    ]