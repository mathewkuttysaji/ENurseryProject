from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact_us_view, name='contact'), 
    path('user_home', views.user_home, name="user_home"), 
    path('add_to_cart', views.add_to_cart, name='add_to_cart'), 
    path('view_cart', views.view_cart, name="view_cart"), 
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'), 
    path('update_cart_quantity/<int:product_id>/<int:quantity>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('purchase_next', views.purchase_next, name='purchase_next'), 
    path('make_purchase', views.make_purchase, name="make_purchase")
]