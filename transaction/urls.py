from django.urls import path
from . import views

urlpatterns = [
    path('vendas/', views.sales_index, name='sales'),
    path('vendas/vender', views.sell, name='sell'),
    path('vendas/carrinho', views.sale_cart, name='sale-cart'),
    path('compras/', views.purchases_index, name='purchases'),
    path('compras/comprar', views.buy, name='buy'),
    path('compras/carrinho', views.buy_cart, name='buy-cart'),
]