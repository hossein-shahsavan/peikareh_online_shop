from django.urls import path, re_path
from . import views


app_name = 'shop'
urlpatterns = [
    path('search/', views.search.as_view(), name='search'),
    re_path(r'product/(?P<slug>[-\w]+)/', views.RetrieveProductView.as_view(), name='product_detail'),
    path('', views.Home.as_view(), name='home'),

]
