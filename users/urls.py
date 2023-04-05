from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from . import views
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'users'

urlpatterns = [
	path('register/', views.registration, name="registration"),
	path('login/', views.signin, name="signin"),
	path('logout/', views.signout, name="signout"),
	    path('password-reset/',
			auth_views.PasswordResetView.as_view(
			template_name='store/password_reset.html'
			), name="password_reset"),
	path('password-reset/done/',
			auth_views.PasswordResetDoneView.as_view(
			template_name='store/password_reset_done.html'
			), name="password_reset_done"),
	path('password-reset-confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'),
            name='password_reset_confirm'),
	path('<str:username>/', views.profile, name="profile"),
	path('contributions/<str:username>/', views.contributions, name="contributions"),
	path('contribute/<slug:slug>/', views.get_contribution, name="cont-profile"),
	path('withdaw/<slug:slug>/', views.widthdrawal, name="withdrawal"),
	# path('profile/', views.cont_page, name="cont-page"),
]
