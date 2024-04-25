from django.contrib import admin
from django.urls import path, include
from eaglemark import views
from eaglemark.views import edit_package, delete_package,update_package


urlpatterns = [
    path('',views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('signout', views.signout, name="signout"),
    path('tracker', views.tracker, name="tracker"),
    path('help', views.help, name="help"),
    path('admin', views.admin, name="admin"),
    path('add_package', views.add_package, name="add_package"),
    path('package_list', views.package_list, name="package_list"),
    path('edit_package/<str:mark>/', edit_package, name='edit_package'),
    path('delete_package/<str:mark>/', delete_package, name='delete_package'),
    path('update_package/<str:MARK>/',update_package, name='update_package')
    ]
