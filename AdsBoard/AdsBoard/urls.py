
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from ads.views import PostList, HomePageView, AboutPageView, ContactsPageView
from accounts.views import SignupPageView, LoginPageView, LogoutPageView, ConfirmEmailPageView, MyPasswordChangeView, MyPasswordResetView

urlpatterns = [

    path('admin/', admin.site.urls),

    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('posts/', include('ads.urls')),

    path('account/signup/', SignupPageView.as_view(), name='account_signup'),
    path('account/login/', LoginPageView.as_view(), name='account_login'),
    path('account/logout/', LogoutPageView.as_view(), name='account_logout'),
    path('account/password/change/', MyPasswordChangeView.as_view(), name='account_change_password'),
    path('account/password/reset/', MyPasswordResetView.as_view(), name='account_reset_password'),
    path('account/', include('allauth.urls')),
    path('account/', include('accounts.urls')),

    path('', PostList.as_view()),

]
