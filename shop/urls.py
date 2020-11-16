from django.urls import path, re_path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    re_path(r'product/(?P<slug>[-\w]+)/', views.RetrieveProductView.as_view(), name='product_detail'),
    path('comment/add/', views.AddComent, name='add_comment'),

]
