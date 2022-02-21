from cgitb import lookup
from posixpath import basename
from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

cartitem_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cartitem_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + cartitem_router.urls
