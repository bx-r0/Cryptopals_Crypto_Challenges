from django.urls import path
import webServer.views as views
import webServer.SRPServer as SRPServer

urlpatterns = [
    path("", views.index, name='index'),
    path('challenge31', views.challenge31, name='challenge31'),
    path('challenge32', views.challenge32, name='challenge32'),
    path('challenge41', views.challenge41, name='challenge41'),
    path('SRP/action', SRPServer.action, name='SRP.action')
]
