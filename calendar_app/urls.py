from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    path('', views.calendar_home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/neu/', views.event_create, name='event_create'),
]