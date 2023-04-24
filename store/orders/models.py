import os

from django.db import models


class Order(models.Model):
    order_name = models.CharField(max_length=30, unique=True, verbose_name="Order name", )

    class Status(models.TextChoices):
        NEW = 'New', 'New'
        PROCESS = 'In Process', 'In Process'
        STORED = 'Stored', 'Stored'
        COMPLETE = 'Complete', 'Complete'

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
    )

    linked_account = models.ForeignKey(
        os.getenv('LINKED_APP'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=os.getenv('LINKED_APP') + ' account'
    )

    def __str__(self) -> str:
        return f"{self.order_name} - {self.linked_account} - {self.status}"


class Store(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Store account", primary_key=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Warehouse account", primary_key=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Token(models.Model):
    linked_name = models.ForeignKey(os.getenv('LINKED_APP'), on_delete=models.DO_NOTHING)
    my_name = models.ForeignKey(os.getenv('MY_APP'), on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.token}"
