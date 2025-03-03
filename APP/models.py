#from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)  
    mot_de_passe = models.CharField(max_length=50)

class FormDataSupervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    full_name = models.CharField(max_length=300)  
    date_enregistrement = models.DateField(null=True, blank=True)
    lieu_activite = models.CharField(max_length=100, blank=True, null=True)

    stock_sim_activees = models.PositiveIntegerField(null=True, blank=True)
    stock_sim_blanches = models.PositiveIntegerField(null=True, blank=True)
    sim_appro = models.PositiveIntegerField(null=True, blank=True)

    effectif_total = models.PositiveIntegerField(null=True, blank=True)
    effectif_present = models.PositiveIntegerField(null=True, blank=True)

    gsm = models.PositiveIntegerField(null=True, blank=True)
    momo_app = models.PositiveIntegerField(null=True, blank=True)
    mymtn = models.PositiveIntegerField(null=True, blank=True)
    ayoba = models.PositiveIntegerField(null=True, blank=True)

    telephone = models.PositiveIntegerField(null=True, blank=True)
    modem = models.PositiveIntegerField(null=True, blank=True)
    mifi = models.PositiveIntegerField(null=True, blank=True)
    wifix = models.PositiveIntegerField(null=True, blank=True)

    difficultes = models.TextField(blank=True, null=True)
    momoconvertion = models.PositiveIntegerField(blank=True, null=True)
    resetpin = models.PositiveIntegerField(blank=True, null=True)
    prospection = models.TextField(blank=True, null=True)
    besoin = models.TextField(blank=True, null=True)
    concurrentielle = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"

class MoMoPayMassMarket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    full_name = models.CharField(max_length=300)  
    date_enregistrement = models.DateField(null=True, blank=True)
    date_creation = models.DateField() 
    heure_creation = models.TimeField()  
    nom_merchant = models.CharField(max_length=255)  
    nom_etablissement = models.CharField(max_length=255)  
    localisation_merchant = models.CharField(max_length=255)  
    reference_adresse = models.TextField(blank=True, null=True)  
    secteur_activite = models.CharField(max_length=100)  
    numero_merchant = models.CharField(max_length=50, unique=True)  
    identifiant_merchant = models.CharField(max_length=50, unique=True)  
    montant_transaction = models.DecimalField(max_digits=15, decimal_places=2)  

    date_created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.full_name} - {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"

from django.contrib.auth.models import User
from django.db import models

class RAPPORT_GSM(models.Model):
    superviseur = models.ForeignKey(User, on_delete=models.CASCADE)
    données = models.TextField()  

    class Meta:
        permissions = [
            ("can_view_all_gsm", "Peut voir tous les rapports GSM"),
            ("can_view_own_gsm", "Peut voir ses propres rapports GSM"),
            ("can_view_all", "Peut voir tous les rapports (GSM et MoMoPay)"),  # Directeur Général
        ]

class RAPPORT_MOMOPAY(models.Model):
    superviseur = models.ForeignKey(User, on_delete=models.CASCADE)
    données = models.TextField()  

    class Meta:
        permissions = [
            ("can_view_all_momopay", "Peut voir tous les rapports MoMoPay"),
            ("can_view_own_momopay", "Peut voir ses propres rapports MoMoPay"),
            ("can_view_all", "Peut voir tous les rapports (GSM et MoMoPay)"),  # Directeur Général
        ]
