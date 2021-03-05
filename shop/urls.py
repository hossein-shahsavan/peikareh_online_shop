from django.urls import path, re_path
from . import views


app_name = 'shop'
urlpatterns = [
    path('search/', views.search.as_view(), name='search'),
    path('popular/', views.ProductPopularFilterView.as_view(), name='popular'),
    re_path(r'product/(?P<slug>[-\w]+)/', views.RetrieveProductView.as_view(), name='product_detail'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.ProductCategoryFilterView.as_view(), name='category_filter'),
    path('', views.Home.as_view(), name='home'),

]
