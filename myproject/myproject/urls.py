from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('1/', views.search_movie),
    path('2/', views.search_relation),
    path('3/', views.search_ask),
    path('4/', views.search_recommendation),
    path('5/', views.search_details),
]
