from django.urls import path
from . import views
urlpatterns = [
    path('',views.register,name='register'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('homepage/',views.homepage,name='homepage'),
    path('profile/',views.profilepage,name='profilepage'),
    path('question/',views.question,name='question'),
    path('vote/<poll_id>',views.vote,name='vote'),
    path('result/<poll_id>',views.result,name='result'),

]