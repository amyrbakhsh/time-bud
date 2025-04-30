from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/signup/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/<int:user_id>/', views.profile, name='profile'),

    path('watches/<int:watch_id>/', views.watch_detail, name='watch_detail'),

    path('watches/create/', views.WatchCreate.as_view(), name='watch_create'),

    path('watches/<int:pk>/update/', views.WatchUpdate.as_view(), name='watch_update'),
    
    path('watches/<int:pk>/delete/', views.WatchDelete.as_view(), name='watch_delete'),
]


