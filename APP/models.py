from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)  
    mot_de_passe = models.CharField(max_length=50)

class FormDataSupervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    full_name = models.CharField(max_length=300)  
    date_enregistrement = models.DateField(null=True, blank=True)
    lieu_activite = models.CharField(max_length=100, choices=[
        ("Lieu 1", "Lieu 1"),
        ("Lieu 2", "Lieu 2"),
        ("Lieu 3", "Lieu 3"),
        ("Lieu 4", "Lieu 4"),
        ("Lieu 5", "Lieu 5")
    ])
    stock_sim_activees = models.PositiveIntegerField(null=True, blank=True)
    stock_sim_blanches = models.PositiveIntegerField(null=True, blank=True)
    sim_appro = models.PositiveIntegerField(null=True, blank=True)

    effectif_total = models.PositiveIntegerField(null=True, blank=True)
    effectif_present = models.PositiveIntegerField(null=True, blank=True)

    gsm = models.PositiveIntegerField(null=True, blank=True)
    momo_app = models.PositiveIntegerField(null=True, blank=True)
    mymtn = models.PositiveIntegerField(null=True, blank=True)

    telephone = models.PositiveIntegerField(null=True, blank=True)
    modem = models.PositiveIntegerField(null=True, blank=True)
    mifi = models.PositiveIntegerField(null=True, blank=True)
    wifix = models.PositiveIntegerField(null=True, blank=True)

    difficultes = models.TextField(blank=True, null=True)
    prospection = models.TextField(blank=True, null=True)
    besoin = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"

