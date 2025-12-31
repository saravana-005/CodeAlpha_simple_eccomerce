from django.urls import path
from watch import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home/",views.home,name="home"),
    path("search/",views.search_products,name="search"),
    path("smart",views.smart_search,name="smart"),
    path("product/<str:category>/",views.product_list,name="products"),
    path("add/<int:product_id>/",views.add_to_cart,name="add"),
    path("view",views.view_cart,name="view_cart"),
    path("increase/<int:item_id>/",views.increase,name="increase"),
    path("decrease/<int:item_id>/",views.decrease,name="decrease"),
    path("remove/<int:item_id>/",views.remove,name="remove"),
    path('',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/", views.order_success, name="order_success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
