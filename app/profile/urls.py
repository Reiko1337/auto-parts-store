from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='account_login'),
    path('profile/', views.ProfileView.as_view(), name='account_profile'),
    path('profile/update/', views.ProfileUpdate.as_view(), name='account_profile_update'),
    path('email/', views.show_404, name='account_email'),


    path('list-order/', views.OrderHistory.as_view(), name='list_order'),
    path('orders/detail/<int:id>/', views.OrderHistoryDetail.as_view(), name='order_detail'),
    path('address/', views.AddressUserView.as_view(), name='address'),
    path('address/add/', views.AddressUserAddView.as_view(), name='address_add'),
    path('address/update/<int:id>/', views.AddressUserUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:id>/', views.AddressUserDeleteView.as_view(), name='address_delete'),

    path('chekout/', views.CheckoutView.as_view(), name='checkout'),
    path('chekout/address/<int:id>/', views.CheckoutAddressUser.as_view(), name='checkout_address_user'),
]
