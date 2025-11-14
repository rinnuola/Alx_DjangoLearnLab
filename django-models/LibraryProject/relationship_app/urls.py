from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),

    # Role-based views (updated)
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

    # Other app features
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
