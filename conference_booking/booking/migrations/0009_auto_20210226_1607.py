# Generated by Django 3.0 on 2021-02-26 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_remove_room_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='room',
            old_name='caption',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.AddField(
            model_name='slot',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Room'),
        ),
        migrations.AddField(
            model_name='slot',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
