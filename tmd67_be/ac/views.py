from django.contrib.auth.models import User
from rest_framework import exceptions, mixins, permissions, status, viewsets
from rest_framework.response import Response

from .serializers import CreateIdentitySerializer, RetrieveIdentitySerializer


class ACIDRegister(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CreateIdentitySerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _tmp = User(**serializer.data)
        if User.objects.filter(email=_tmp.email).exists():
            raise exceptions.ValidationError(
                {
                    "email": [
                        "This email was registered; please use forgot password to reset it."
                    ]
                }
            )

        user = User(**serializer.data)
        user.username = _tmp.email
        user.set_password(_tmp.password)
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ACIDDirectory(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = RetrieveIdentitySerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(
            self.serializer_class(
                request.user, context=self.get_serializer_context()
            ).data
        )
