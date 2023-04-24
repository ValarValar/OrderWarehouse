from functools import cache
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order, Token
from .serializers import OrderSerializer, OrderUpdateSerializer

@cache
def get_token(request: Request) -> Optional[Token]:
    token_header = request.headers.get("token")
    try:
        return Token.objects.get(token=token_header)
    except ObjectDoesNotExist:
        return None


class HasToken(BasePermission):
    def has_permission(self, request, view):

        if token := get_token(request):
            if request.data.get('linked_account') == token.my_name.name:
                return True
        return False


class WebhookViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [HasToken, ]


class OrderWebhookViewSet(WebhookViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_name'

    def modify_data_by_token(self, request: Request) -> dict:
        """
            Заменяет атрибут linked account на полученный по токену
            и возвращает новый словарь с данными
        """
        token = get_token(request)
        data = dict(**request.data)
        data['linked_account'] = token.linked_name.name
        return data

    def create(self, request: Request, *args, **kwargs):
        modified_data = self.modify_data_by_token(request)

        serializer = self.get_serializer(data=modified_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, order_name=None, *args, **kwargs):
        modified_data = self.modify_data_by_token(request)

        serializer = OrderUpdateSerializer(data=modified_data)
        serializer.is_valid(raise_exception=True)

        self.queryset.filter(
            order_name=order_name
        ).update(
            status=modified_data['status'],
            linked_account=modified_data['linked_account']
        )
        return Response(status=status.HTTP_200_OK)
