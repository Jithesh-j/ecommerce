from django.urls import path
from . import views


urlpatterns = [
    # path("", views.PaymentPage.as_view(), name = "payments"),
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('paymentsuccess/',views.paymentsuccess, name='paymentsuccess'),

] 
