from django.urls import path

from . import views
urlpatterns = [
    path('cards/', views.display_cards, name='cards'),
    path('', views.login, name='login'),
    path('start/', views.start, name='start'),

]