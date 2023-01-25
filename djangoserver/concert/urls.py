from django.urls import path
from . import views

app_name = 'concert'
urlpatterns = [
    path(route='', view=views.get_concert_list_view, name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<int:pk>/', views.ConcertDetailView.as_view(), name='details'),
    path('<int:concert_id>/register/', views.register, name='concert_register'),
]