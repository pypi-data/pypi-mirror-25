from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^track-product-visit.js$', views.track_product_visit, name='track-product-visit'),
    url(r'^visited-products/$', views.visited_products, name='visited-products'),
]
