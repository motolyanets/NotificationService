from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from user.views import UserViewSet
from message.views import GeneralStatisticsViewSet, SpecificStatViewSet
from newsletter.views import NewsletterViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("newsletters", NewsletterViewSet)
router.register("statistics", GeneralStatisticsViewSet)
router.register("statistics", SpecificStatViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
