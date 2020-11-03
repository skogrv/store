from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from store import views

urlpatterns = [
    path('', views.home, name='store-home'),
    path('create_listing', views.create_listing, name='create_listing'),
    path('listings', views.listings, name='listings'),
    path('favourite<int:id>', views.favourite, name='favourite'),
    path('order<int:id>', views.order_detail, name='order'),
    path('favourite_orders', views.favourite_list, name='favourite_orders'),
    path('remove<int:id>', views.delete_order, name='remove'),
    path('order_edit<int:pk>', views.EditOrder.as_view(), name='edit_order'),
    path('delete_comment<int:pk>', views.delete_comment, name='delete_comment'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('like<int:id>', views.like, name='like'),

]
