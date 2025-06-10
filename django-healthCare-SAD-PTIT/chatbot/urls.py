from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),
    path('new_session/', views.new_session, name='new_session'),
]