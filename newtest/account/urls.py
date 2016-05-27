from django.conf.urls import url, include
from .views import all_users, add_user, save_user, after_login_home, login, logout, forgot_password, reset_password, signup, activate

urlpatterns = [
    url(r'^all/$', all_users),
    url(r'^add/$', add_user),
    url(r'^save/$', save_user),
    url(r'^(?P<id>\d+)/home/$', after_login_home, name="home"),
    url(r'^login/$',login, name="login"),
    url(r'^logout/$',logout, name="logout"),
    url(r'^signup/$',signup, name="signup"),
    url(r'^forgot-password/$',forgot_password, name="forgot-password"),
    url(r'^reset-password/(?P<id>\d+)/(?P<otp>\d{4})/$',reset_password, name="reset-password"),
    url(r'^activate-account/(?P<id>\d+)/(?P<otp>\d{4})/$',activate, name="activate-account"),

]