"""
URLs for ideas app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('idea/<int:pk>/', views.idea_detail, name='idea-detail'),
    path('like/<int:pk>/', views.like_idea, name='like-idea'),
    path('comment/<int:pk>/', views.add_comment, name='add-comment'),
    path('create/', views.create_idea, name='create-idea'),
]
