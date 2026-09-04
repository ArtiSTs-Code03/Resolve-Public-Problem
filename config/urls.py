from django.contrib import admin
from django.urls import path
from complaints import views

urlpatterns = [
    # Admin Panel (RePuP Desk)
    path('admin/', admin.site.urls),

    # Direct Dashboard Root URL
    path('', views.dashboard, name='dashboard'),

    # Optional Login/Logout agar baad me zaroorat pade
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Complaint Management
    path('raise/', views.raise_complaint, name='raise_complaint'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
]