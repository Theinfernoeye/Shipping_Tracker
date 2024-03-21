from django.contrib import admin
from django.urls import path, include
from eaglemark import views

urlpatterns = [
    path('',views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('signout', views.signout, name="signout"),
    path('tracker', views.tracker, name="tracker"),
    path('help', views.help, name="help"),
    path('admin', views.admin, name="admin"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('add_package', views.add_package, name="add_package"),
    path('package_list', views.package_list, name="package_list")
    ]
