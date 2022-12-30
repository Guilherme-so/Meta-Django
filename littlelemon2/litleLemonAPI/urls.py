from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('category', views.CategoryView),
    path('menu-items', views.MenuItems),
    path('secret/', views.Secret),
    path('api-token-auth/', obtain_auth_token), # para gerar token automatic com username e password
    path('manager/', views.menager),
    path('throttle_check/', views.throttle_check), #limitar o acesso para para anonimos
    path('throttle_check_auth/', views.throttle_check_auth), #limitar o acesso para para users logados
    path('groups/manager/users/', views.managers)
    # path('menu-items/<int:pk>', views.SingleMenuItem.as_view())
]