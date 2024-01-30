from django.urls import path

from ncm_app.views import PageView
from posts.views import PostDetailView, PostListView

urlpatterns = [
    # path('page/<slug:slug>/', PageView.as_view(), name='page_view'),
    path('post/list/', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

    # Другие маршруты, если необходимо
]
