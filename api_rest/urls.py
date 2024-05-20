from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_users, name='get_all_users'),
    path('user/<str:nick>', views.get_by_nick),
    path('user/nick', views.get_by_nick_by_body),
    path('age/more/<int:age>', views.get_by_age_more_than),
    path('age/under/<int:age>', views.get_by_age_under_than),
    path('data/', views.user_manager)
]
