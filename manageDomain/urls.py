from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from manageDomain import views


urlpatterns = [
    # path('delete_domain/', views.delete_domain),
    # path('add_domain/', views.add_domain),
    # path('update_domain/', views.update_domain),
    # path('update_entity_attr/', views.update_entity_attr),
    # path('update_relation_attr/', views.update_relation_attr),
    path('get_label_list/', views.get_label_list),
    path('get_domain_list/', views.get_domain_list),
    # path('get_attr_list/', views.get_attr_list),
    # path('add_attr/', views.add_attr),
    # path('update_attr/', views.update_attr),
    # path('delete_attr/', views.delete_attr)
]