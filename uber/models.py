from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django import forms

class Vehicle(models.Model):
    ID = models.AutoField(primary_key = True) 
    vehicle_type = models.CharField(max_length=250,default="")
    vehicle_make = models.CharField(max_length=250,default='')
    vehicle_model = models.CharField(max_length=250,default='')
    passenger_capacity = models.IntegerField()
    luggage_capacity = models.IntegerField()
    vehicle_image= models.FileField()
    is_favourite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('uber:detail', kwargs={"pk": self.pk})
    

    # no need to use migration for __str__() class, because you are not adding/deleting columns/rows in database
    def __str__(self):
        return self.vehicle_type+" - "+self.vehicle_make+" - "+self.vehicle_model


class Driver(models.Model):
    
    ssn = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=200,default="")
    last_name = models.CharField(max_length=250,default="")
    sex = models.CharField(max_length=50,default="")
    birth_day = models.DateField(null=True, auto_now=False, auto_now_add=False, default='')
    vehicle_id = models.ManyToManyField(Vehicle)
    is_favourite= models.BooleanField(default= False)
    driver_image= models.FileField()

    def get_absolute_url(self):
        return reverse('uber:all_driver', kwargs={"pk": self.pk})

    def __str__(self):
        return self.first_name + self.last_name +" - "+ self.sex



class Customer(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=500, default="1@gmail.com")
    first_name = models.CharField(max_length=200,default="")
    last_name = models.CharField(max_length=250,default="")
    sex = models.CharField(max_length=50,default="")

    def __str__(self):
        return self.first_name+" "+self.last_name+" - "+self.sex

# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Customer.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile, sender=User)

class Ride(models.Model):
    #ID = models.AutoField(primary_key=True)
    #customer_id =  models.OneToOneField(Customer, primary_key=True,default="",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver_ssn = models.ForeignKey(Driver,on_delete=models.CASCADE)
    starting_location = models.CharField(max_length=500,default="")
    destination = models.CharField(max_length=500,default="")
    starting_time = models.CharField(max_length=500, default="")
    ending_time = models.CharField(max_length=500,default="")
    fare = models.IntegerField()
    
    def __str__(self):
        return self.starting_location+" "+self.destination

# class Feedback(models.Model):
#     ID = models.AutoField(primary_key= True)
#     customer_email = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE)
#     driver_ssn = models.ForeignKey(Driver, on_delete=models.CASCADE)
#     safety = models.IntegerField()
#     customer_service = models.IntegerField()
#     clean = models.IntegerField()
#     overall = models.IntegerField()

#     def __str__(self):
#         return self


# class Coupon(models.Model):
#     #ID = models.AutoField()
#     customer_email = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     discount = models.IntegerField()

#     def __str__(self):
#         return self

# class Customer_GPS(models.Model):
#     customer_email = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     location = models.CharField( max_length=250,default="")
#     time_stamp= models.DateTimeField(primary_key=True, auto_now=False, auto_now_add=False)

#     def __str__(self):
#         return self

# class Vehicle_GPS(models.Model):
#     vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     location = models.CharField( max_length=250,default="")
#     time_stamp= models.DateTimeField(primary_key=True, auto_now=False, auto_now_add=False)

#     def __str__(self):
#         return self