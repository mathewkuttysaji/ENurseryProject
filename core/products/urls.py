from django.urls import path
from . import views 


urlpatterns = [
    path('product_upload',  views.product_upload, name="product_upload"), 
    path('update_product', views.update_product, name="update_product"), 
]
