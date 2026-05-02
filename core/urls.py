# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='member_list'),
    path('member/<int:pk>/', views.member_detail, name='member_detail'),
    path('generate-certificate/<int:member_id>/', views.generate_certificate, name='generate_certificate'),
    path('leadership/', views.leadership, name='leadership'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('videos/', views.videos, name='videos'),

    path('news/', views.news, name='news'),
    path('trainings/', views.trainings, name='trainings'),
    path('achievements/', views.achievements, name='achievements'),
    path('rating/', views.rating, name='rating'),
    path('join/', views.join, name='join'),
]