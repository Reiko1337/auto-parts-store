from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'store'

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),

    path('list/auto-part/', views.ListAutoPart.as_view(), name='list_auto_part'),
    path('list/auto-part/filter/', views.AutoPartFilter.as_view(), name='list_auto_part_filter'),
    path('list/auto-part/<slug:brand>/', views.ListAutoPart.as_view(), name='list_auto_part_brand'),
    path('list/auto-part/<slug:brand>/<slug:model>/', views.ListAutoPart.as_view(), name='list_auto_part_brand_model'),
    path('detail/auto-part/<slug:brand>/<slug:model>/<slug:category>/<slug:slug>/', views.DetailAutoPart.as_view(), name='detail_auto_part'),

    path('list/kit-car/', views.ListKitCar.as_view(), name='list_kit_car'),
    path('list/kit-car/filter/', views.KitCarFilter.as_view(), name='list_kit_car_filter'),
    path('list/kit-car/<slug:brand>/', views.ListKitCar.as_view(), name='list_kit_car_brand'),
    path('list/kit-car/<slug:brand>/<slug:model>/', views.ListKitCar.as_view(), name='list_kit_car_brand_model'),
    path('detail/kit-car/<slug:brand>/<slug:model>/<slug:slug>/', views.DetailKitCar.as_view(), name='detail_kit_car'),


    path('list/wheel/', views.ListWheel.as_view(), name='list_wheel'),
    path('list/wheel/filter/', views.WheelFilter.as_view(), name='list_wheel_filter'),
    path('list/wheel/<slug:brand>/', views.ListWheel.as_view(), name='list_wheel_brand'),
    path('list/wheel/<slug:brand>/<slug:model>/', views.ListWheel.as_view(), name='list_wheel_brand_model'),
    path('detail/wheel/<slug:brand>/<slug:model>/<slug:slug>/', views.DetailWheel.as_view(), name='detail_wheel'),

    path('filter-models/', views.FilterModelsGenerate.as_view(), name='filter_models'),

    path('cart/add/<str:model>/<str:id>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/delete/<str:model>/<str:id>/', views.DeleteItemInCart.as_view(), name='delete_from_cart'),
]
