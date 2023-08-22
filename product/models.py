from django.db.models import *


class Product(Model):
    name = CharField(max_length=255, null=False)

