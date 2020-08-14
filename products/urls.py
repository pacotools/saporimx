from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),

    # The product id should be an integer since otherwise navigating to
    # products/add will interpret the string add as a product id which
    # will cause that view to throw an error. This happens because django
    # will always use the first URL it finds a matching pattern for and in
    # this case unless we specify that product id is an integer django
    # doesn't know the difference between a product number and a string
    # like add.

    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product,
         name='delete_product'),
]
