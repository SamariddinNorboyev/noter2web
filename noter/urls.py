from django.urls import path
from . import views
app_name='noter'
urlpatterns = [
    path('', views.Home, name='home'),
    path('upcoming/', views.Upcoming, name='upcoming'),
    path('sticky-wall/', views.StickyWall, name='sticky-wall'),
    path('calendar/', views.Calendar, name='calendar'),
    path('history/', views.History, name='history'),


    path('create-list/', views.CreateList, name='create-list'),
    path('lists/<int:list_id>/', views.ShowList, name='lists'),


    path('create-note/', views.CreateNote, name='create-note'),
    path('do/<int:note_id>/', views.do, name='do'),
    path('update/<int:note_id>/', views.update, name='update'),
    path('delete/<int:note_id>/', views.delete, name='delete'),
]