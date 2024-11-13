from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('answer/', views.answer, name='answer'),
	path('hot/', views.hot, name='hot'),
	path('error/', views.error, name='error'),
]
