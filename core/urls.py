from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.item_list, name="item_list"),
    path("items/report-lost/", views.item_create_lost, name="item_create_lost"),
    path("items/report-found/", views.item_create_found, name="item_create_found"),
    path("items/<int:pk>/", views.item_detail, name="item_detail"),
    path("items/<int:pk>/edit/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("items/<int:pk>/toggle-status/", views.item_toggle_status, name="item_toggle_status"),
]