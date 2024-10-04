from rest_framework.routers import DefaultRouter
from django.urls import path
from tracker.apps import TrackerConfig
from tracker.views import WayViewSet, WayPublicListAPIView

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r'way', WayViewSet, basename='way')

urlpatterns = [
    path('way-public-list/', WayPublicListAPIView.as_view(), name='way_public_list'),
] + router.urls
