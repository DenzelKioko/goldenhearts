from django.urls import path
from . import views

# Sets the namespace for this app, required for {% url 'donations:donate' %}
app_name = 'donations'

urlpatterns = [
    # URLs for the three different donation types, matching the names used in base.html
    path('money/', views.donation_form_view, {'donation_type': 'money'}, name='donate_money'),
    path('items/', views.donation_form_view, {'donation_type': 'items'}, name='donate_items'),
    path('service/', views.donation_form_view, {'donation_type': 'service'}, name='donate_service'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]