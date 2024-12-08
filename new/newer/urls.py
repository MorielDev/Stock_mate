from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'), # new URL path for the index page
    path('signin/', views.signin, name='signin'),
    path('add/', views.add, name='add'),
    path('home/', views.home, name='home'),
    path('edit/<int:item_id>/', views.edit, name='edit'),
    path('categories/', views.categories, name='categories'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Add URL for the dashboard
    path('profile/', views.profile, name='profile'),  # URL pattern for the profile page
    path('viewStocks/', views.my_stocks, name='viewStocks'),  # URL pattern for the my stocks page
    path('', views.home, name='root'),  # Add a root URL to point to the home page
]
