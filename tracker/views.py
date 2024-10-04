from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from tracker.models import Way
from tracker.paginators import TrackerPaginator
from tracker.serializers import WaySerializer, WayPublicSerializer
from users.permissions import IsOwner


class WayViewSet(viewsets.ModelViewSet):
    serializer_class = WaySerializer
    queryset = Way.objects.all()
    pagination_class = TrackerPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        way = Way.objects.filter(owner=self.request.user)
        return way


class WayPublicListAPIView(generics.ListAPIView):
    serializer_class = WayPublicSerializer
    queryset = Way.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = TrackerPaginator

    def get_queryset(self):
        way = Way.objects.filter(is_public=True)
        return way
