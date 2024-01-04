from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.view_products, name='view_products'),
    path('view_users', views.view_users, name="view_users"), 
    path('view_purchases', views.view_purchases, name='view_purchases'), 
    path('view_purchase_details', views.purchase_details, name='view_purchase_details')
]
