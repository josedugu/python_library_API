from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import action
from book.serializers import BookSerializer, BookItemSerializer, BookItemSerializerRetrieve
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from book.models import Book, BookItem

from .permisions import IsLibrarian
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status



class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['name', 'author', 'category']
    search_fields = ['author']


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer

    # permission_classes = [IsLibrarian]
    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookItemSerializerRetrieve
        else:
            return BookItemSerializer

    @action(detail=False)
    def list_rent_books(self, request):
        books_items = BookItem.objects.filter(
            is_rent=True
        )
        serializer = BookItemSerializer(books_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["patch"], detail=True)
    def set_user_rent(self, request, pk):
        book_item = BookItem.objects.get(pk=pk)
        if book_item.reserve == None or book_item.reserve == User.objects.get(pk=request.data["rent"]):
            books_items = Book.objects.filter(bookitem__rent_id=request.data["rent"]).count()
            if books_items >= 2:
                return Response({"message": "No puedes rentar mas de 2 libros"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(
                BookItem.objects.get(pk=pk),
                data=request.data, partial=True)
            if serializer.is_valid():

                self.perform_update(serializer)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Este libro esta reservado por otra persona"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["patch"], detail=True)
    def set_user_reserve(self, request, pk):
        serializer = self.serializer_class(
            BookItem.objects.get(pk=pk),
            data=request.data, partial=True)
        if serializer.is_valid():

            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     print(request.data["rent"])
    #     books_items = BookItem.objects.filter(rent_id=request.data["rent"]).count()
    #     if books_items > 2:
    #         return Response({"message": "No puedes rentar mas de 2 libros"}, status=status.HTTP_400_BAD_REQUEST)
    #     serializer = self.serializer_class(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)