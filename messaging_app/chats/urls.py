from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create DRF router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

# Include router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
