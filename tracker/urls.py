from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import WayViewSet

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r'way', WayViewSet, basename='way')

urlpatterns = [
] + router.urls
