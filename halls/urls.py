from django.urls import path
from .views import book_view, block_view, floor_rooms, room_view, book_space, all_view, explore_hostel, un_book


urlpatterns = [
    path('', all_view, name='index'),
    path('explore/<str:hall_name>', explore_hostel, name='explore'),
    path('hostel', book_view, name='hostel'),
    path('<str:hall>/blocks', block_view, name='blocks'),
    path('floor/<str:slug>', floor_rooms, name='floor'),
    path('room/<str:slug>', room_view, name='room'),
    path('book/<str:pos>/<str:pk>', book_space, name='book'),
    path('cancel/booking/<str:pos>/<str:pk>', un_book, name='un_book'),
]
