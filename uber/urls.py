from django.conf.urls import url 
from django.urls import path
from .import views
#from .views import IndexView
from django.contrib.auth import login, logout

from django.conf.urls import  include, url
from django.contrib.auth.decorators import login_required

#from .views import search

app_name= 'uber'

urlpatterns = [

    # /uber/
    #url(r'^$',views.IndexView.as_view(), name='index'),

    path('', views.IndexView.as_view(), name='index'),

    path('drivers/', views.DriverIndexView.as_view(), name='driver_index'),
    #path('', views.index, name='index'),
    path('results/', views.search, name="search"),
    path('all_rides/', views.RidesView.as_view(), name='all_rides'),



    # /uber/712/
    path('<pk>/',views.DetailView.as_view(), name= 'detail'),

    url(r'^(?P<driver_id>[0-9]+)/favourite/$', views.favourite, name='favourite'),

    url(r'^(?P<vehicle_id>[0-9]+)/favourite_vehicle/$', views.favourite_vehicle, name='favourite_vehicle'),

    #url(r'^(?P<vehicle_id>[0-9]+)/(?P<driver_id>[0-9]+)/$', views.ride, name='ride'),

    url(r'^(?P<vehicle_id>[0-9]+)/(?P<driver_id>[0-9]+)/$', views.RideView.as_view(), name='ride'),
    url(r'^(?P<vehicle_id>[0-9]+)/(?P<driver_id>[0-9]+)/ride_details/$', views.ride_details, name='ride_details'),

 

    #uber/vehicle/add
    path('vehicle/add/', views.VehicleCreate.as_view(), name='create_vehicle'),

    #uber/vehicle/2/
    path('vehicle/<pk>/', views.VehicleUpdate.as_view(), name='update_vehicle'),

    #uber/vehicle/2/delete/
    path('vehicle/<pk>/delete/', views.VehicleDelete.as_view(), name='delete_vehicle'),


    #uber/all_driver/
    path('all_driver/<pk>/', views.driver_detail, name='all_driver'),

    #path('all_driver/', views.driver_view, name='all_driver'),

    # #uber/driver/add
    path('driver/add/', views.DriverCreate.as_view(), name='create_driver'),

    # #uber/driver/2/
    path('driver/<pk>/', views.DriverUpdate.as_view(), name='update_driver'),

    # #uber/driver/2/delete/
    path('driver/<pk>/delete/', views.DriverDelete.as_view(), name='delete_driver'),



]


