
from django import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/',include('autapi.urls')),
    path('v2/',include('jwtauth.urls')),

]
