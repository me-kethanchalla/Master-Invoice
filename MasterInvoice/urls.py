from django.contrib import admin
from django.urls import path, include
from user.views import login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('inventory/', include('inventory.urls')),
    path('inward_supply/', include('inward_supply.urls'),name="inward_supply_list"),
    path('outward_supply/', include('outward_supply.urls')),
    path('analysis/', include('analysis.urls')),
    path('transactions/', include('transactions.urls')),
]
 