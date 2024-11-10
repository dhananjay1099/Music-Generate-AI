from django.urls import path
from . import views

app_name = 'music_gen'

urlpatterns = [
    path('', views.generate_music_view, name='generate'),
    path('check_status/<int:track_id>/', views.check_status, name='check_status'),
] 