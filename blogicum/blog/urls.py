from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostView.as_view(), name='index'),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:pk>/comment/', views.add_comment,
         name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:pk1>/',
         views.edit_comment,
         name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:pk1>/',
         views.delete_comment,
         name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<slug:username>/', views.profile_detail, name='profile'),
    path('profile/<slug:username>/edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),

]
 