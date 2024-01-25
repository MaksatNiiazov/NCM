# ваш_app/urls.py
from django.urls import path
from .views import PageView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('page/<slug:slug>/', PageView.as_view(), name='page_view'),
]
