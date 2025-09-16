from django.urls import path, register_converter
from .views import index_view, pricing_view, orders, dashboard, profile_view, login_view, signup_view, wallet, logout_view, fund_wallet, call_back, callback_view, profile_edit
from libs.number_libs.us import getnumber, getnumber_list, rent_number

class ServiceConverter:
    regex = '[\w\.]+' 

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

register_converter(ServiceConverter, 'service')



urlpatterns = [
    path('', index_view, name='index'),
    path('login', login_view, name='login'),
    path('signup', signup_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('wallet', wallet, name='Wallet'),
    path('profile/', profile_view, name='profile'),
    path('checkout', fund_wallet, name='checkout'),
    path('callback', callback_view, name="callback-page"),
    path('payment/verify', call_back, name='call-back'),
    path('pricing', pricing_view, name='pricing'),
    path('dashboard', dashboard, name='Dashboard'),
    path('orders', orders, name='Order'),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path('api/services/us/numbers', getnumber_list, name="all-other-numbers"),
    path('api/services/us/numbers/rent/request/<str:number_id>', rent_number, name='request-rent-us'),
    # Us number service
    path(
        'api/services/us/numbers/<service:service>/', 
        getnumber, 
        name='getnumber'
    )
]