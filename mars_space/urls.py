from django.urls import path
from .views import post_detail, like_post, create_post, home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('create_post/', create_post, name='create_post'),
]
