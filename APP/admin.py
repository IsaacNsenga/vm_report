from django.contrib import admin
from django.contrib.auth.models import Group
from .models import RAPPORT_GSM, RAPPORT_MOMOPAY

class RAPPORT_GSMAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.has_perm('APP.can_view_all'):  
            return qs  # Directeur Général voit tout
        elif request.user.has_perm('APP.can_view_all_gsm'):
            return qs  # Responsable GSM voit tout
        elif request.user.has_perm('APP.can_view_own_gsm'):
            return qs.filter(superviseur=request.user)  # Utilisateur GSM voit ses propres données
        return qs.none()

class RAPPORT_MOMOPAYAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.has_perm('APP.can_view_all'):  
            return qs  # Directeur Général voit tout
        elif request.user.has_perm('APP.can_view_all_momopay'):
            return qs  # Responsable MoMoPay voit tout
        elif request.user.has_perm('APP.can_view_own_momopay'):
            return qs.filter(superviseur=request.user)  # Utilisateur MoMoPay voit ses propres données
        return qs.none()

admin.site.register(RAPPORT_GSM, RAPPORT_GSMAdmin)
admin.site.register(RAPPORT_MOMOPAY, RAPPORT_MOMOPAYAdmin)


