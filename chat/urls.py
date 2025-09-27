from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('faq-dashboard/', views.faq_dashboard, name='faq_dashboard'),
    path('faq/delete/<int:faq_id>/', views.delete_faq, name='delete_faq'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
