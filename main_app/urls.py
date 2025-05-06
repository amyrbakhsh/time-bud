from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/signup/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),

   
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('tags/<int:tag_id>/', views.tag_list, name='tag_list'),

   
    path('watches/<int:pk>/', views.watch_detail, name='watch_detail'),

    path('watches/create/', views.WatchCreate.as_view(), name='watch_create'),

    path('watches/<int:pk>/update/', views.WatchUpdate.as_view(), name='watch_update'),
    
    path('watches/<int:pk>/delete/', views.WatchDelete.as_view(), name='watch_delete'),

path('watches/<int:watch_id>/start-auction/', views.start_auction, name='start_auction'),


     path('bids/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),

     path('transactions/', views.my_transactions, name='my_transactions'),


]


