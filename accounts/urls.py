from django.urls import path

from .views import (
    register,
    login,
    logout,
    change_password,
)

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('change-password/', change_password),
]