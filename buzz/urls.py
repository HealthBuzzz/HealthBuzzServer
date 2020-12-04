from django.urls import path
from buzz import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('year/stretching/', views.stretchingdata, name='stretchingdata'),
    path('year/water/', views.waterdata, name='waterdata'),
    path('today/', views.today),
    path('today/refresh/', views.today_refresh),
    path('today/stretching/', views.today_stretching),
    path('today/water/', views.today_water),
    path('token/', views.token, name='token'),
]
