"""taxicab_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from uber import views
from django.conf import settings 
from django.conf.urls.static import static 

from django.contrib.auth import login, logout
#from django.contrib.auth import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^uber/',include('uber.urls', namespace='uber')), # include url from other file (e.g. uber/urls.py)

    path('', views.home, name='home'),

    path('auth/',include('django.contrib.auth.urls')),
    path('auth/signup/', views.UserFormView.as_view(), name='signup'),
    path('auth/profile/', views.view_profile, name='view_profile'),
    path('auth/profile/edit/',views.edit_profile, name='edit_profile'),
    path('auth/change-password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('auth/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset/done',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    url(r'^auth/password_reset/confirm/(?P<uib64>[0-9A-Za-z]+)-(?P<token>.+)/$',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'^auth/password_reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
