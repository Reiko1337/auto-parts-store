from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'store'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),

    path('auto-parts/', views.ListAutoParts.as_view(), name='auto_parts'),
    path('auto-parts/filter/', views.AutoPartFilter.as_view(), name='auto_parts_filter'),
    path('auto-parts/<slug:brand>/', views.ListAutoParts.as_view(), name='auto_parts_model'),
    path('auto-parts/<slug:brand>/<slug:model>/', views.ListAutoParts.as_view(), name='auto_parts_model'),
    path('auto-parts/detail/<slug:brand>/<slug:model>/<slug:auto_part>/', views.DetailAutoPart.as_view(), name='detail_auto_parts'),

    path('wheels-drive/', views.ListWheelsDrive.as_view(), name='wheels_drive'),
    path('wheels-drive/filter/', views.WheelDriveFilter.as_view(), name='wheels_drive_filter'),
    path('wheels-drive/<slug:brand>/', views.ListWheelsDrive.as_view(), name='wheels_drive'),
    path('wheels-drive/<slug:brand>/<slug:model>/', views.ListWheelsDrive.as_view(), name='wheels_drive'),
    path('wheels-drive/detail/<slug:brand>/<slug:model>/<slug:wheel_drive>/', views.DetailWheelDrive.as_view(), name='detail_wheels_drive'),

    path('kits-car/', views.ListKidsCar.as_view(), name='kids_car'),
    path('kits-car/filter/', views.KidCarFilter.as_view(), name='kits_car_filter'),
    path('kits-car/<slug:brand>/', views.ListKidsCar.as_view(), name='kids_car'),
    path('kits-car/<slug:brand>/<slug:model>/', views.ListKidsCar.as_view(), name='kids_car'),
    path('kits-car/detail/<slug:brand>/<slug:model>/<int:id>/', views.DetailKidCar.as_view(), name='detail_kits_car'),

    path('filter-models/', views.FilterModelsGenerate.as_view()),

    path('cart/add/<str:model>/<str:id>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/delete/<str:model>/<str:id>/', views.DeleteItemInCart.as_view(), name='delete_from_cart'),

    path('test/', views.TestView.as_view())
]
