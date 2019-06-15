"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordResetView, PasswordResetConfirmView,
)
from django.shortcuts import redirect
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from .views import permission_denied, register

login_params = {
    'template_name': 'user/login.html',
    'redirect_authenticated_user': True,
}

password_reset_params = {
    'template_name': 'user/password_reset.html',
    'email_template_name': 'user/password_reset/email.html',
    'subject_template_name': 'user/password_reset/subject.txt',
    'success_url': reverse_lazy('login'),
}

password_set_params = {
    'template_name': 'user/password_set.html',
    'post_reset_login': True,
    'success_url': reverse_lazy('root'),
}

urlpatterns = [
    path('', lambda request: redirect('staff:index'), name='root'),
    path('login/', LoginView.as_view(**login_params), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('password-reset/', 
         PasswordResetView.as_view(**password_reset_params), 
         name='password_reset'),
    path('password-set/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(**password_set_params),
         name='password_set'),

    path('staff/', include('staff.urls')),
    path('customer/', include('customer.urls')),
    path('account/', include('account.urls')),
    path('transaction/', include('transaction.urls')),
    path('earlyknow/', include('earlyknow.urls')),
    path('api/', include('api.urls')),
    path('recognize/', include('recognize.urls')),
    
    path('admin/', admin.site.urls),
] + static('images/', document_root=settings.IMAGE_ROOT)