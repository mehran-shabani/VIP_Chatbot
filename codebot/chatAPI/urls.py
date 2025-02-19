from django.urls import path
from .views import custom_login_view, custom_logout_view, chat_request

urlpatterns = [
    path('login/', custom_login_view, name='custom_login'),
    path('logout/', custom_logout_view, name='custom_logout'),
    path('chat/', chat_request, name='chat_request'),
]
