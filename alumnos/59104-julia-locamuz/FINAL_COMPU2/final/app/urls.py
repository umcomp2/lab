from django.urls import path, include
from rest_framework import routers
from .models import *
from .views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'cliente', ClienteViewSet)
router.register(r'compra', CompraViewSet)
router.register(r'establecimiento', EstablecimientoViewSet)
router.register(r'item', ItemViewSet)
router.register(r'show', ShowViewSet)

# Wire up our API using automatic URL routing.

urlpatterns = [
    path('', include(router.urls)),
]