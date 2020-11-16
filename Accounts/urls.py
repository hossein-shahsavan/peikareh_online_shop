from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('<int:pk>/', views.ProfileRetrieveUpdateView.as_view(), name='profile'),

]