from django.urls import path
from shop import views
from django.contrib.auth import views as  auth_views
from .forms import LoginForm,UserPasswordChangeForm,UserPasswordResetForm,UserSetPasswordForm



urlpatterns = [
   
   
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
  
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('registration', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html',authentication_form=LoginForm),name='login'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='shop/changepassword.html',form_class=UserPasswordChangeForm, success_url='/changepassworddone/'),name='changepassword'),
    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(template_name='shop/changepassworddone.html'),name='changepassworddone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='shop/passwordreset.html',form_class=UserPasswordResetForm),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='shop/passwordresetdone.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='shop/passwordresetconfirm.html',form_class=UserSetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='shop/passwordresetcomplete.html'),name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    
    
]
