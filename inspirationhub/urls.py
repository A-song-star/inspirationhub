"""
URL configuration for inspirationhub project.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ideas import views as idea_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', idea_views.home, name='home'),
    path('idea/<int:pk>/', idea_views.idea_detail, name='idea-detail'),
    path('idea/like/<int:pk>/', idea_views.like_idea, name='like-idea'),
    path('idea/comment/<int:pk>/', idea_views.add_comment, name='add-comment'),
    path('idea/create/', idea_views.create_idea, name='create-idea'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
]
