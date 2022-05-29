from rest_framework.serializers import ModelSerializer
from .models import Book, BookItem
from core.serializers import UserSerializer


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookItemSerializer(ModelSerializer):
    book = BookSerializer
    class Meta:
        model = BookItem
        fields = "__all__"

class BookItemSerializerRetrieve(ModelSerializer):
    book = BookSerializer()
    rent = UserSerializer()

    class Meta:
        model = BookItem
        fields = "__all__"