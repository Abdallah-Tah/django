from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('login_endpoint/', views.login_endpoint, name='login_endpoint'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register_user'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
