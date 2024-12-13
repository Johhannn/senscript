from django.urls import path
from . import views
from .views import ProfileListView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('projects/<int:profile_id>/', views.get_projects_for_profile, name='get_projects_for_profile'),
]
