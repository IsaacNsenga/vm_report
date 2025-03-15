from django.contrib import admin
from django.urls import path
from APP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.connexion, name='connexion'),
    path('passwordreset/', views.passwordreset, name='passwordreset'),
    path('home/', views.home, name='home'),
    path('gsm/', views.gsm, name='gsm'),
    path('momopay/', views.momopay, name='momopay'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('rapport_gsm/', views.rapport_gsm, name='rapport_gsm'),
    path('rapport_momopay/', views.rapport_momopay, name='rapport_momopay'),
    path('download_momopay_report/', views.download_momopay_report, name='download_momopay_report'),
    path('download_gsm_report/', views.download_gsm_report, name='download_gsm_report'),
]
