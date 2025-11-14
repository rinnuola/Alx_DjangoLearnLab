from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # <-- ADDED
from . import views
from .views import list_books, register, LibraryDetailView  # <-- ENSURE ALL ARE IMPORTED

urlpatterns = [
    # 🌟 FIX FOR 404 ERROR 🌟 
    path('', views.list_books, name='home'), 
    
    # --- Authentication Paths ---
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name='relationship_app/login.html'), name="login"),
    
    # CORRECTED TYPO: It was 'LogoutView.as_as_view'
    path("logout/", LogoutView.as_view(template_name='relationship_app/logout.html'), name="logout"), 
    
    # --- New Task Paths ---
    path('books/', views.list_books, name='list_books'), 
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]