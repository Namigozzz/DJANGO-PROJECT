from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )


    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )


    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        open_advertisements_count = Advertisement.objects.filter(
            creator=self.context["request"].user,
            status='OPEN'
        ).count()

        if open_advertisements_count >= 10:
            raise serializers.ValidationError('У вас слишком много объявлений')

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного объявления."""

    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Favorite
        fields = ('user', 'advertisement')


    def validate(self, data):
        if data['advertisement'].creator == self.context['request'].user:
            raise serializers.ValidationError('Нельзя добавить своё объявление в избранное')

        return data
