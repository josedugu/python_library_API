from django.contrib import admin
from .models import Book, BookItem
# Register your models here.

admin.site.register(Book)
admin.site.register(BookItem)