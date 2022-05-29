from django.contrib.auth.models import User
from django.db import models
import  uuid
# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=240)
    author = models.CharField(max_length=180)
    tema = models.CharField(max_length=180)
    isbn = models.CharField(max_length=11)
    category = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class BookItem(models.Model):
    rack = models.CharField(max_length=4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False)
    reserve = models.ForeignKey(User, on_delete=models.CASCADE,
                                default=None,
                                null=True,
                                blank=True,
                                related_name="reserve")
    is_reserve = models.BooleanField(default=False)
    rent = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=None, null=True, blank=True,
                             related_name="rent")
    is_rent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.name} - {self.rack}"