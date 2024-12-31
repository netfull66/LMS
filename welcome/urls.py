from django.urls import path
from .views import register, login_view, logout_view,profile_view

urlpatterns = [
    path('register/', register, name='register_school'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

]
