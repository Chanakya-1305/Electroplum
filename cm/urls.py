from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('inveter/', views.inveter, name='inveter'),
    path('plumbers/', views.plumbers, name='plumbers'),
    path('exploreus/', views.exploreus, name='exploreus'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),
    path('ac/', views.ac, name='ac'),
    path('booking/', views.booking, name='booking'),
    path('electricalservices/', views.electricalservices, name='electricalservices'),
    path('logout/', views.logout, name='logout'),
    path('employeeregistration/', views.employeeregistration, name='employeeregistration'),
    path('get_workers/', views.get_workers, name='get_workers'),
    path('bookingconfirmationpage/', views.bookingconfirmationpage, name='bookingconfirmationpage'),
    path('bookinghistorypage/', views.bookinghistorypage, name='bookinghistorypage'),
    path('cancelbookingpage/<int:booking_id>/', views.cancelbookingpage, name='cancelbookingpage'),
    path('newlogin/', views.newlogin, name='newlogin'),
    path('employee-login/', views.employee_login, name='employee_login'),
    path('employee-dashboard/', views.employee_dashboard,name='employee_dashboard'),
    path('ourwork/', views.ourwork, name='ourwork'),
    path( 'employee-dashboard/',  views.employee_dashboard, name='employee_dashboard'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path( 'reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
]