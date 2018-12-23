from django.urls import path
import webServer.views as views

urlpatterns = [
    path("", views.index, name='index'),
    path('challenge31', views.challenge31, name='challenge31'),
    path('challenge32', views.challenge32, name='challenge32'),
]
