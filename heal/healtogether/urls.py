from django.contrib import admin
from django.urls import path, include
from . import views
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path('', include("heal.urls")), 
# ]
urlpatterns = [ 
    path('', views.index, name = "home"), 
    path('login', views.login, name = "login"), 
    path('logout', views.logout, name = "logout"), 
    path('nearest_lab/', views.get_nearest_lab, name='nearest_lab'),
] 
