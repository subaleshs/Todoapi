from django import views
from django.urls import path
from .views import *
from rest_framework.authtoken import views as authview

urlpatterns = [

    path('api/users/', ListUsers.as_view()),
    path('api/token/', authview.obtain_auth_token),
    path('api/works/', AddViewTodo.as_view()),
    path('api/signup/', SignUp.as_view()),
    path('api/login/', LogIn.as_view()),
    path('api/update/<int:itemKey>/', UpdateTodo.as_view()),
    
]
