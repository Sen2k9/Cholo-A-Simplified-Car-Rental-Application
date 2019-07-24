
from django.shortcuts import render, get_object_or_404 # shortcuts for HttpResponse, and get an object or show 404 response
from .models import Vehicle, Driver, Customer, Ride #importing required model
from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserForm, EditProfileForm, RideForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView

#from django.contrib.auth.forms import UserForm

# def driver_view(request):
#     drivers = Driver.objects.all()
#     return render(request, 'uber/all_driver.html',{'drivers':drivers})


def home(request):
    #plans = FitnessPlan.objects
    return render(request, 'home.html')

def view_profile(request):
    args = {'user': request.user}
    return render(request, 'registration/profile.html',args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/auth/profile/')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'registration/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) #to restore the session of previous user after changing password
            return redirect('/auth/profile/')

        else:
            return redirect('auth/change-password/')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'registration/change_password.html', args)




@login_required
def ride(request,vehicle_id,driver_id):
    vehicle =  get_object_or_404(Vehicle, pk=vehicle_id)
    driver = get_object_or_404(Driver, pk=driver_id)
    #customer = get_object_or_404(Customer, pk=customer_id)
    

    form = RideForm(request.POST or None)
    if form.is_valid():
        ride = form.save()
        ride.user = request.user
        #ride.customer_id = customer
        ride.vehicle_id = vehicle
        ride.driver_ssn = driver

        ride.save()
    args = {'form':form,'vehicle':vehicle,'driver':driver}

    return render(request,'uber/ride.html',args)


class RideView(TemplateView):
    template_name = 'uber/ride.html'

    def get(self, request,vehicle_id,driver_id):
        form = RideForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request,vehicle_id,driver_id):
        vehicle =  get_object_or_404(Vehicle, pk=vehicle_id)
        driver = get_object_or_404(Driver, pk=driver_id)
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            ride.vehicle_id = vehicle
            ride.driver_ssn = driver

            ride.save()
            starting_location = form.cleaned_data['starting_location']
            destination = form.cleaned_data['destination']
            starting_time = form.cleaned_data['starting_time']
            ending_time = form.cleaned_data['ending_time']
            fare = form.cleaned_data['fare']
            form = RideForm()
            #return redirect('uber:ride.html')

        args = {
            'vehicle':vehicle,
            'driver':driver,
            
            'form':form,
            'starting_location':starting_location,
            'destination':destination,
            'starting_time':starting_time,
            'ending_time':ending_time,
            'fare':fare
            }
        return render(request, 'uber/ride_details.html', args)





@login_required
def ride_details(request,vehicle_id,driver_id):

    
    vehicle =  get_object_or_404(Vehicle, pk=vehicle_id)
    driver = get_object_or_404(Driver, pk=driver_id)
    #customer = get_object_or_404(Customer, pk=customer_id)
    #ride = Ride.objects.get(pk=ride_id)
    #customer = Customer.objects.all()
    rides = Ride.objects.all()


    args = {'vehicle':vehicle,'driver':driver,'rides':rides}

    return render(request,'uber/ride_details.html',args)


# def all_rides(request):
#     rides = Ride.objects.all()
#     for ride in rides:
#         if ride.user == request.user:
#             new_ride = ride
#             break
    

#     #user = User.objects.get(pk=request.user)
#     return render(request,'uber/all_rides', {'new_ride':new_ride})


class RidesView(generic.ListView):
    template_name = 'uber/all_rides.html'
    context_object_name = 'rides'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RidesView, self).dispatch(*args, **kwargs)

    # def get(self):
    #     rides = Ride.objects.all()
    #     for ride in rides:
    #         if ride.user is request.user:
    #             current_ride = ride

    #     return render(request, self.template_name, {'current_ride':current_ride})

    def get_queryset(self):
        return Ride.objects.all()


class IndexView(generic.ListView):
    template_name = 'uber/index.html'
    context_object_name = 'vehicles'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Vehicle.objects.all()
    



class DriverIndexView(generic.ListView):
    template_name = 'uber/driver_index.html'
    context_object_name = 'drivers'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DriverIndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Driver.objects.all()

def search(request):
    template = 'uber/search_results.html'

    query = request.GET.get('q')

    vehicles = Vehicle.objects.filter(
    Q(vehicle_make=query)|
    Q(vehicle_model=query)|
    Q(vehicle_type=query)).distinct()

    drivers = Driver.objects.filter(
    Q(first_name=query)|
    Q(sex=query)|
    Q(last_name=query)).distinct()

    return render(request, template,
    {
        'vehicles':vehicles,
        'drivers': drivers,
    })

    

# def index(request):

    
#     vehicles = Vehicle.objects.filter(request.user)
#     driver_results = Driver.objects.all()
#     query = request.GET.get("q")
#     if query:
#         vehicles = vehicles.filter(
#             Q(vehicle_make__icontains=query) |
#             Q(vehicle_model__icontains=query)
#         ).distinct()
#         driver_results = driver_results.filter(
#             Q(first_name__icontains=query)
#         ).distinct()
#         return render(request, 'uber/index.html', {
#             'vehicles': vehicles,
#             'drivers': driver_results,
#         })
#     else:
#         return render(request, 'uber/index.html', {'vehicles': vehicles})


class DetailView(generic.DetailView):
    model = Vehicle
    template_name = 'uber/detail.html'

def favourite(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    try:
        if driver.is_favourite:
            driver.is_favourite = False
        else:
            driver.is_favourite = True
        driver.save()
    except (KeyError, Driver.DoesNotExist):
        return render(request,'uber/all_driver.html',{'driver':driver})

    else:
        return render(request,'uber/all_driver.html',{'driver':driver})


def favourite_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    try:
        if vehicle.is_favourite:
            vehicle.is_favourite = False
        else:
            vehicle.is_favourite = True
        vehicle.save()
    except (KeyError, Vehicle.DoesNotExist):
        return render(request, 'uber/detail.html',{'vehicle':vehicle})
    else:
        return render(request, 'uber/detail.html',{'vehicle':vehicle})
        #return JsonResponse({'success': True})

class VehicleCreate(CreateView):
    model = Vehicle
    
    fields = ['ID','vehicle_type','vehicle_make','vehicle_model','passenger_capacity','luggage_capacity','vehicle_image']

class VehicleUpdate(UpdateView):
    model = Vehicle
    fields = ['ID','vehicle_type','vehicle_make','vehicle_model','passenger_capacity','luggage_capacity','vehicle_image']

class VehicleDelete(DeleteView):
    model = Vehicle
    success_url = reverse_lazy("uber:index")



class DriverDetailView(generic.ListView):
    model = Driver
    template_name = 'uber/all_driver.html'

def driver_detail(request,pk):
    driver = Driver.objects.get(pk=pk)
    return render(request, 'uber/all_driver.html', {'driver':driver})

    def get_queryset(self):
        return Driver.objects.all()


class DriverCreate(CreateView):
    model = Driver
    
    fields = ['ssn', 'first_name', 'last_name', 'sex', 'birth_day', 'vehicle_id', 'is_favourite', 'driver_image']

class DriverUpdate(UpdateView):
    model = Driver
    fields = ['ssn', 'first_name', 'last_name', 'sex', 'birth_day', 'vehicle_id', 'is_favourite', 'driver_image']

class DriverDelete(DeleteView):
    model = Driver
    success_url = reverse_lazy("uber:index")


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    #process from data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password = password)

            if user is not None:

                if user.is_active:

                    login(request,user)
                    return redirect('uber:index')

        return render(request, self.template_name, {'form': form})

