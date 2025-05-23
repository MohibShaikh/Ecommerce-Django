from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.index, name="shop"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('products/<int:myid>', views.productView, name="productView"),
    path('search/', views.search, name="search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('payment-confirmation/', views.payment_confirmation, name="payment_confirmation"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


