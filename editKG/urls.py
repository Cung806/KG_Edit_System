from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from editKG import views


urlpatterns = [
    path('get_entity', views.get_entity),
    path('get_neighbor', views.get_neighbor),
    path('change_kg', views.change_nodel_relation),
    path('delete_relation', views.delete_relation),
    path('delete_startnode', views.delete_startnode),
    path('delete_endnode', views.delete_endnode),
    path('get_label_relation_list', views.get_label_list),
    path('add_in_relation', views.add_in_relation),
    path('add_out_relation', views.add_out_relation),
    path('add_node', views.add_node),
    path('get_detail', views.get_detail),
    path('get_label_relation_list_demo', views.get_label_list_demo),
    path('get_entity_demo', views.get_entity_demo),
    path('get_neighbor_demo', views.get_neighbor_demo),
]