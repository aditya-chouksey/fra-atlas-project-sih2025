from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('api/districts/<int:state_id>/', views.api_districts, name='api_districts'),
    path('api/district-geometry/<int:district_id>/', views.api_district_geometry, name='api_district_geometry'),
    path('api/scheme-recommendations/<int:district_id>/', views.api_scheme_recommendations, name='api_scheme_recommendations'),
]