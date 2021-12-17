from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products'),
    path('categorias/', views.categories, name='categories'),
    path('inserir-categoria/', views.insert_category, name='insert-category'),
    path('utilitarios/', views.utility_list, name='utility-list'),
    path('lista/', views.product_list, name='product-list'),
    path('inserir/', views.insert_product, name='insert-product'),
    path('editar/<int:pk>', views.edit_product, name='edit-product'),
    path('editar-categpria/<int:pk>', views.edit_category, name='edit-category'),
]