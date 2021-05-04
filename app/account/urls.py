from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('orders/', views.OrderHistory.as_view(), name='orders'),
    path('orders/detail/<int:id>/', views.OrderHistoryDetail.as_view(), name='order_detail'),

    path('address/', views.AddressUserView.as_view(), name='address'),
    path('address/add/', views.AddressUserAddView.as_view(), name='address_add'),
    path('address/update/<int:id>/', views.AddressUserUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:id>/', views.AddressUserDeleteView.as_view(), name='address_delete'),

    path('chekout/', views.CheckoutView.as_view(), name='checkout'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:main'), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration')
]
