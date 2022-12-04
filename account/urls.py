from django.urls import path, re_path
from . import views

urlpatterns = [
	path('login/', views.loginPage, name='login'),
	path('createacc/', views.createacc, name='createacc'),
	path('forgotpass/', views.forgotpass, name='forgotpass'),
	path('logout/', views.logout, name='logout'),
	path('reset/', views.reset, name='reset')

]