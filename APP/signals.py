from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import FormDataSupervisor, MoMoPayMassMarket  # Import des modèles liés aux rapports

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # Création des groupes
    gsm_group, created = Group.objects.get_or_create(name="GSM")
    momopay_group, created = Group.objects.get_or_create(name="MoMoPay")
    directeur_group, created = Group.objects.get_or_create(name="Directeur Général")

    # Création des permissions spécifiques
    content_type_gsm = ContentType.objects.get_for_model(FormDataSupervisor)
    content_type_momopay = ContentType.objects.get_for_model(MoMoPayMassMarket)

    permission_gsm = Permission.objects.get_or_create(
        codename="view_all_gsm_reports",
        name="Peut voir tous les rapports GSM",
        content_type=content_type_gsm,
    )[0]

    permission_momopay = Permission.objects.get_or_create(
        codename="view_all_momopay_reports",
        name="Peut voir tous les rapports MoMoPay",
        content_type=content_type_momopay,
    )[0]

    # Attribution des permissions aux groupes
    gsm_group.permissions.add(permission_gsm)
    momopay_group.permissions.add(permission_momopay)
    directeur_group.permissions.add(permission_gsm, permission_momopay)
