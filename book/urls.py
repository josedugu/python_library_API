from rest_framework.routers import DefaultRouter
from .views import BookViewset, BookItemViewSet

router = DefaultRouter()
router.register('books', BookViewset)
router.register('books_items', BookItemViewSet)
urlpatterns = router.urls