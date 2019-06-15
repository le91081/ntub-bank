from django.urls import path
from . import views

app_name = 'recognize'
urlpatterns = [
    path('', views.index, name='index'),
    path('show_user/<str:uuid>/', views.show_user, name='show_user'),
]
