from rest_framework import serializers

from .models import Badge, Order, Ticket


class ReprMixin:
    @staticmethod
    def to_representation(instance):
        return {
            "id": instance.id,
            "account_identifier": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
        }


class CreateIdentitySerializer(ReprMixin, serializers.Serializer):
    email = serializers.EmailField(help_text="*required")
    password = serializers.CharField(
        max_length=50, min_length=6, help_text="*required"
    )
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RetrieveIdentitySerializer(ReprMixin, serializers.Serializer):
    identity = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    state = serializers.CharField(max_length=10, read_only=True)
    amount = serializers.IntegerField(
        max_value=2147483647, min_value=0, read_only=True, default=0
    )
    created_time = serializers.DateTimeField(read_only=True, allow_null=True)
    badge_set = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Badge.objects.all()
    )

    class Meta:
        model = Order
        fields = ["id", "user", "state", "amount", "created_time", "badge_set"]


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"
