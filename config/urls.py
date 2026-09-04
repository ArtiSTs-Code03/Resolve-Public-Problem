from django.contrib import admin
from django.urls import path, include
from complaints import views  # ya aapka home page jis view me hai

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root path ("") ko home page par point karein:
    path('', views.home, name='home'),  
    
    # Login page ke liye alag se URL banayein:
    path('login/', views.login_view, name='login'),
    
    # Baki URLs
    path('raise/', views.raise_complaint, name='raise_complaint'),
]