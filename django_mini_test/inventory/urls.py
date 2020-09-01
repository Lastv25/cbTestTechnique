from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('add/', views.item_create),
    path('<int:pk>/delete_item/', views.delete_item, name="delete_item"),
    path('<int:pk>/modify_item/', views.modify_item, name="modify_item")
]
