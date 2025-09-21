from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# ALX expects this exact router instantiation
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
