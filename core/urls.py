from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('write/', views.post, name='write'),
    path('settings/update_profile', views.update_profile, name='update_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('settings/profile/<int:pk>', views.profile, name='profile'),
    path('full-post/<int:pk>', views.full_post, name="full-post"),
    path('edit/<int:pk>', views.edit_post, name='edit'),
    path("art/", views.art_view, name="art"),
    path("science", views.sci_view, name="science"),
    path("technology", views.tech_view, name="technology")
]
