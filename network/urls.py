from django.urls import path
from . import views


app_name = 'network'

urlpatterns = [
    path('', views.home, name='home'),
    path('post_detail/<uuid:post_id>', views.post_detail, name='post_detail'),
    path('like/', views.like, name='like'),
    path('comment/', views.comment, name='comment'),
]
