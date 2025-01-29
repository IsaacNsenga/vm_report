from django.contrib import admin
from django.urls import path
from APP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('rapport/', views.rapport, name='rapport'),
]
