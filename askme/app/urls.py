from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('answer/<str:question_id>', views.answer, name='answer'),
	path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('error/', views.error, name='error'),
    path('site_404/', views.error, name='site_404'),
]
