from django.urls import path
from buzz import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('waterdata/', views.waterdata, name='waterdata'),
    path('stretchingdata/', views.stretchingdata, name='stretchingdata'),
    path('today/', views.today),
    path('today/stretching/', views.today_stretching),
    path('today/water/', views.today_water),
    path('token/', views.token, name='token'),
]
