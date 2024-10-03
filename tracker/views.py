from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tracker.models import Way
from tracker.serializers import WaySerializer


class WayViewSet(viewsets.ModelViewSet):
    serializer_class = WaySerializer
    queryset = Way.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
