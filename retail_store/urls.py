from django.urls import path, include
from .views import cashier, inventory, manager, staff 

urlpatterns = [
    path('staff/', include(([
            path('user_login/', staff.user_login, name="login"),
            path('register/', staff.register_business, name='register_business'),
            path('business_login/', staff.business_login, name='business_login'),
            path('dashboard/', staff.user_dashboard, name='user_dashboard'),
            path('select_user/', staff.user_selector, name='user_selector'),
            path("generate_cashier_login/", staff.generate_cashier_login, name="generate_cashier_login"),
            path("cashier_login/", staff.cashier_login, name="cashier_login"),
    ], 'retail_store'), namespace = 'staff')),
]


