from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name == "APP":  # Remplace "APP" par le nom exact de ton app Django
        # Création des groupes
        groups_permissions = {
            "GSM Responsable": ["can_view_all_gsm"],
            "GSM Utilisateur": ["can_view_own_gsm"],
            "MoMoPay Responsable": ["can_view_all_momopay"],
            "MoMoPay Utilisateur": ["can_view_own_momopay"],
            "Directeur Général": ["can_view_all"],
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_code in permissions:
                try:
                    permission = Permission.objects.filter(codename=perm_code).first()
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"⚠️ Permission {perm_code} introuvable ! Exécute `makemigrations` et `migrate`.")

