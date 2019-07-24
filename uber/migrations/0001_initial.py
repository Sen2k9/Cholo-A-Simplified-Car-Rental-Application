# Generated by Django 2.2.3 on 2019-07-24 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(default='1@gmail.com', max_length=500)),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=250)),
                ('sex', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('ssn', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=250)),
                ('sex', models.CharField(default='', max_length=50)),
                ('birth_day', models.DateField(default='', null=True)),
                ('is_favourite', models.BooleanField(default=False)),
                ('driver_image', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('vehicle_type', models.CharField(default='', max_length=250)),
                ('vehicle_make', models.CharField(default='', max_length=250)),
                ('vehicle_model', models.CharField(default='', max_length=250)),
                ('passenger_capacity', models.IntegerField()),
                ('luggage_capacity', models.IntegerField()),
                ('vehicle_image', models.FileField(upload_to='')),
                ('is_favourite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_location', models.CharField(default='', max_length=500)),
                ('destination', models.CharField(default='', max_length=500)),
                ('starting_time', models.CharField(default='', max_length=500)),
                ('ending_time', models.CharField(default='', max_length=500)),
                ('fare', models.IntegerField()),
                ('driver_ssn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uber.Driver')),
                ('user', models.ForeignKey(default='', editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uber.Vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='vehicle_id',
            field=models.ManyToManyField(to='uber.Vehicle'),
        ),
    ]