from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from client.views import ClientViewSet
from message.views import MessageViewSet
from newsletter.views import NewsletterViewSet

router = SimpleRouter()
router.register("clients", ClientViewSet)
router.register("newsletters", NewsletterViewSet)
router.register("messages", MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
]
