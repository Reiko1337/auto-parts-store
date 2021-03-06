from django.urls import path
from . import views
from .admin_filter import views as views_admin

app_name = 'store'

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),

    path('list/spare-part/<str:chapter>/', views.ListSparePart.as_view(), name='list_spare_part'),
    path('list/spare-part/<str:chapter>/filter/', views.SparePartFilter.as_view(), name='list_spare_part_filter'),
    path('list/spare-part/<str:chapter>/<slug:brand>/', views.ListSparePart.as_view(), name='list_spare_part_brand'),
    path('list/spare-part/<str:chapter>/<slug:brand>/<slug:model>/', views.ListSparePart.as_view(), name='list_spare_part_brand_model'),
    path('detail/spare-part/<slug:brand>/<slug:model>/<slug:category>/<slug:slug>/', views.DetailSparePart.as_view(), name='detail_spare_part'),

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

    path('list/tire/', views.ListTire.as_view(), name='list_tire'),
    path('list/tire/filter/', views.TireFilter.as_view(), name='list_tire_filter'),
    path('detail/tire/<slug:slug>/', views.DetailTire.as_view(), name='detail_tire'),

    path('search/', views.SearchResultView.as_view(), name='search'),


    path('ajax/filter-models/', views.FilterModelsGenerate.as_view(), name='ajax_filter_models'),

    path('cart/add/<str:model>/<str:id>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/delete/<str:model>/<str:id>/', views.DeleteItemInCart.as_view(), name='delete_from_cart'),


    path('admin-filter/ajax/load-categories/', views_admin.load_categories, name='admin_filter_ajax_load_categories'),
    path('admin-filter/ajax/load-brands/', views_admin.load_brands, name='admin_filter_ajax_load_brands'),
    path('admin-filter/ajax/load-models/', views_admin.load_models, name='admin_filter_ajax_load_models'),
]
