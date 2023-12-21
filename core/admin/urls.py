from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.admin_home, name="admin_home"),
    path('view_users', views.view_users, name="view_users"),
    path('view_products', views.view_products, name='view_products')

]
