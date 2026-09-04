from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from complaints import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('raise/', views.raise_complaint, name='raise_complaint'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)