
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path,include
from django.contrib.auth import authenticate, views as  auth_view
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
from app1.forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    path("", views.home, name = "home"),
    path("registration/", views.CustomerRegistrationView.as_view(), name = "registration"),
    path("accounts/login/", auth_view.LoginView.as_view(template_name = "app1/Login.html",
    authentication_form = LoginForm) , name = "Login"),
    path('logout/',auth_view.LogoutView.as_view(next_page = "Login"), name = "logout"),
    path("passwordchange/", auth_view.PasswordChangeView.as_view(template_name = "app1/change_passwords.html", form_class =  MyPasswordChangeForm), name = "changepassword"),
    path("changepassworddone/",auth_view.PasswordChangeDoneView.as_view(template_name = "app1/changepassworddone.html"), name = "password_change_done"),
    path("cart/",views.cart, name = "cart"),
    path("password-reset/",auth_view.PasswordResetView.as_view(template_name = "app1/password-reset.html", form_class = MyPasswordResetForm), name = "password_reset"),
    path("password-reset-done/",auth_view.PasswordResetDoneView.as_view(template_name = "app1/password_reset_done.html"), name = "password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name = "app1/password_reset_confirm.html", form_class = MySetPasswordForm), name = "password_reset_confirm"),
    path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(template_name = "app1/password_reset_complete.html"), name = "password_reset_complete"),
    path("profile/", views.profileView.as_view(), name = "profile"),
    path("orders/", views.orders, name = "orders"),
    path("address/", views.address, name = "address"),
    path("checkout/", views.checkout, name = "checkout"),
    path("product_detail/<int:id>", views.product_detail, name = "product_detail"),
    path("mobiles/", views.mobiles, name = "mobiles"),
    path("mobiles/<slug:data>/", views.mobiles, name = "mobiles"),
    #path("laptops/", views.l, name = "laptops"),
    path("top_wears/", views.top_wears, name = "top_wears"),
    path("top_wears/<slug:data>/", views.top_wears, name = "top_wears"),
    path("bottom_wears/", views.bottom_wears, name = "bottom_wears"),
    path("bottom_wears/<slug:data>/", views.bottom_wears, name = "bottom_wears"),
    path("add-to-cart/",views.show_cart, name = "add-to-cart"),
    path("pluscart/", views.plus_cart, name = "plus_cart"),
    path("minuscart/", views.minus_cart, name = "minus_cart"),
    path("removecart/", views.remove_cart),
    path("paymentdone/", views.paymentdone, name = "paymentdone"),
    path("delete_cart/<int:pk>/", views.delete_cart, name = "delete_cart"),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)