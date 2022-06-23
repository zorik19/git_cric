from django.urls import path
from . import views
urlpatterns = [

 path('', views.users, name="users"),
 path("signup/", views.SignUp.as_view(), name="signup"),
]