from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='auth_register'),
    path('login/', views.loginUser, name='auth_login'),
    path('apps/', views.getApps, name="get_all_apps"),
    path('create_app/', views.createApp, name="create_new_app"),
    path('update_app/<int:pk>/', views.updateApp, name="update_app"),
    path('app/<int:pk>/delete/', views.deleteApp, name="delete_app"),
    path('subscriptions/', views.getSubscriptions, name="get_all_subscriptions"),
    path('update_sub/', views.updateSubscription, name="update_subscription"),
]