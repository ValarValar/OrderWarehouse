import os

import requests
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Order
from .serializers import OrderSerializer

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


@receiver(post_save, sender=Order)
def order_create_update_signal(sender, instance: Order, created, **kwargs):
    headers = {'token': os.getenv('TOKEN')}

    serialized_data = OrderSerializer(instance).data
    post_url = f'{WEBHOOK_URL}/order_webhooks/order/'
    patch_url = f'{WEBHOOK_URL}/order_webhooks/order/{instance.order_name}/'
    if created:
        requests.post(post_url, json=serialized_data, headers=headers)
    else:
        requests.patch(patch_url, json=serialized_data, headers=headers)


@receiver(post_delete, sender=Order)
def order_delete_signal(sender, instance: Order, **kwargs):
    headers = {'token': os.getenv('TOKEN')}
    delete_url = f'{WEBHOOK_URL}/order_webhooks/order/{instance.order_name}/'

    requests.delete(delete_url, headers=headers)
