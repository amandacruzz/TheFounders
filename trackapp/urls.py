from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('donate/', views.donate, name='donate'),
	path('privacy/', views.privacy, name= 'privacy'),
	path('terms/', views.terms, name= 'terms'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('positions/', views.positions, name='positions'),
	path('deletePosition/<str:pk>/', views.deletePosition, name='deletePosition'),
	path('contact/', views.contact, name= 'contact'),
	path('about/', views.about, name='about'),
	path('notcreated/', views.notcreated, name='notcreated'),
	path('preview/', views.preview, name='preview'),
	path('faqs/', views.faqs, name='faqs'),
	path('sponsor/', views.sponsor, name='sponsor'),
]