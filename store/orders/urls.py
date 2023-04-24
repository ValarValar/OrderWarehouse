from rest_framework.routers import DefaultRouter

from .views import OrderWebhookViewSet

router = DefaultRouter()
router.register(r'order', OrderWebhookViewSet, basename='order')
urlpatterns = router.urls
