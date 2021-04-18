from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'store'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),

    path('accounts/login/', views.Login.as_view(template_name='store/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='store:main'), name='logout'),

    path('auto-parts/', views.ListAutoParts.as_view(), name='auto_parts'),
    path('detail_auto_parts/<slug:brand>/<slug:model>/<slug:auto_part>/', views.DetailAutoPart.as_view(), name='detail_auto_parts'),
    path('filter-models/', views.FilterModelsGenerate.as_view()),

    path('add-item-in-cart/<str:id>/', views.AddItemInCart.as_view(), name='add_item_in_cart'),
    path('delete-item-in-cart/<str:id>/', views.DeleteItemInCart.as_view(), name='delete_item_in_cart')
]
