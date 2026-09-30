from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrAdmin, IsOwner
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (Advertisement.objects.filter(
                        status__in=["OPEN", "CLOSED"]
                    ) | Advertisement.objects.filter(
                        status="DRAFT",
                        creator=self.request.user
                    )
                )

        return Advertisement.objects.filter(
            status__in=["OPEN", "CLOSED"]
        )


    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return []


class FavoriteViewSet(ModelViewSet):
    """ViewSet для избранных объявлений."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user,
        )


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
