from django.urls import path
# from django.conf.urls import include
from account import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view),
    path('', views.index),
    path('logout/', views.logout_view),
    path('demo/', views.show_demo)
]
