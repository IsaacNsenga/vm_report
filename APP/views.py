from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FormDataSupervisor, MoMoPayMassMarket
from django.contrib.auth.models import User
import openpyxl
from django.http import HttpResponse

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

def passwordreset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Mot de passe modifié avec succès.')
            except User.DoesNotExist:
                messages.error(request, 'Utilisateur introuvable.')
        else:
            messages.error(request, 'Les deux mots de passe ne correspondent pas.')
    return render(request, 'passwordreset.html')

@login_required
def home(request):
    user = request.user
    
    # Vérifier si l'utilisateur appartient à un groupe spécifique
    is_gsm_user = user.groups.filter(name="GSM Utilisateur").exists()
    is_gsm_responsable = user.groups.filter(name="GSM Responsable").exists()
    is_momopay_user = user.groups.filter(name="MoMoPay Utilisateur").exists()
    is_momopay_responsable = user.groups.filter(name="MoMoPay Responsable").exists()
    is_director = user.groups.filter(name="Directeur Général").exists()

    return render(request, 'index.html', {
        'show_gsm': is_gsm_user or is_gsm_responsable or is_director,  
        'show_momopay': is_momopay_user or is_momopay_responsable or is_director,
    })


@login_required
def gsm(request):
    message = None  # Variable pour stocker le message de succès

    if request.method == 'POST':
        # Récupération des données du formulaire
        date_enregistrement = request.POST.get('date_enregistrement')
        lieu_activite = request.POST.get('lieu_activite')
        stock_sim_activees = request.POST.get('stock_sim_activees')
        stock_sim_blanches = request.POST.get('stock_sim_blanches')
        sim_appro = request.POST.get('sim_appro')

        effectif_total = request.POST.get('effectif_total')
        effectif_present = request.POST.get('effectif_present')

        gsm = request.POST.get('gsm')
        momo_app = request.POST.get('momo_app')
        mymtn = request.POST.get('mymtn')
        ayoba = request.POST.get('ayoba')

        telephone = request.POST.get('telephone')
        modem = request.POST.get('modem')
        mifi = request.POST.get('mifi')
        wifix = request.POST.get('wifix')

        difficultes = request.POST.get('difficultes')
        momoconvertion = request.POST.get('momoconvertion')
        resetpin = request.POST.get('resetpin')
        prospection = request.POST.get('prospection')
        besoin = request.POST.get('besoin')
        concurrentielle = request.POST.get('concurrentielle')

        # Création d'une instance du modèle avec les données récupérées
        form_data = FormDataSupervisor(
            user=request.user,
            full_name=f"{request.user.first_name} {request.user.last_name}",  
            date_enregistrement=date_enregistrement,
            lieu_activite=lieu_activite,
            stock_sim_activees=stock_sim_activees,
            stock_sim_blanches=stock_sim_blanches,
            sim_appro=sim_appro,
            effectif_total=effectif_total,
            effectif_present=effectif_present,
            gsm=gsm,
            momo_app=momo_app,
            mymtn=mymtn,
            ayoba=ayoba,
            telephone=telephone,
            modem=modem,
            mifi=mifi,
            wifix=wifix,
            difficultes=difficultes,
            momoconvertion=momoconvertion,
            resetpin=resetpin,
            prospection=prospection,
            besoin=besoin,
            concurrentielle=concurrentielle
        )

        # Enregistrement des données dans la base de données
        form_data.save()

        # Message de succès
        message = "Formulaire soumis avec succès !"

    return render(request, 'gsm.html', {'message': message})


@login_required
def momopay(request):
    message = None  # Variable pour afficher un message de confirmation

    if request.method == 'POST':
        # Récupération des données du formulaire
        date_enregistrement = request.POST.get('date_enregistrement')
        date_creation = request.POST.get('date_creation')
        heure_creation = request.POST.get('heure_creation')
        nom_merchant = request.POST.get('nom_merchant')
        nom_etablissement = request.POST.get('nom_etablissement')
        localisation_merchant = request.POST.get('localisation_merchant')
        reference_adresse = request.POST.get('reference_adresse')
        secteur_activite = request.POST.get('secteur_activite')
        numero_merchant = request.POST.get('numero_merchant')
        identifiant_merchant = request.POST.get('identifiant_merchant')
        montant_transaction = request.POST.get('montant_transaction')

        # Création d'une instance du modèle avec les données récupérées
        momo_pay = MoMoPayMassMarket(
            user=request.user,
            full_name=f"{request.user.first_name} {request.user.last_name}",  
            date_enregistrement=date_enregistrement,
            date_creation=date_creation,
            heure_creation=heure_creation,
            nom_merchant=nom_merchant,
            nom_etablissement=nom_etablissement,
            localisation_merchant=localisation_merchant,
            reference_adresse=reference_adresse,
            secteur_activite=secteur_activite,
            numero_merchant=numero_merchant,
            identifiant_merchant=identifiant_merchant,
            montant_transaction=montant_transaction
        )

        # Enregistrement des données dans la base de données
        momo_pay.save()

        # Message de succès
        message = "Données enregistrées avec succès !"

    return render(request, 'momopay.html', {'message': message})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def rapport_gsm(request):
    if request.user.has_perm('APP.view_all_gsm_reports'):  
        reports = FormDataSupervisor.objects.all()  # Responsable GSM et DG voient tout
    else:
        reports = FormDataSupervisor.objects.filter(user=request.user)  # Utilisateur normal voit ses propres rapports

    return render(request, 'rapport_gsm.html', {'reports': reports})

@login_required
def rapport_momopay(request):
    if request.user.has_perm('APP.can_view_all_momopay'):
        momopay_reports = MoMoPayMassMarket.objects.all()  # Responsable MoMoPay et DG voient tout
    else:
        momopay_reports = MoMoPayMassMarket.objects.filter(user=request.user)  # Utilisateur normal voit ses propres rapports

    return render(request, 'momopay_rapport.html', {'momopay_reports': momopay_reports})

@login_required
def download_momopay_report(request):
    # Récupère les données à partir du modèle
    if request.user.has_perm('APP.view_all_momopay_reports'):
        momopay_reports = MoMoPayMassMarket.objects.all()  # Responsable MoMoPay et DG voient tout
    else:
        momopay_reports = MoMoPayMassMarket.objects.filter(user=request.user)  # Utilisateur normal voit ses propres rapports

    # Créer un nouveau classeur Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rapport Momopay"

    # Ajouter l'entête du tableau
    header = [
        "Utilisateur", "Nom Complet", "Date Enregistrement", "Date Création", "Heure Création", 
        "Nom du Marchand", "Nom de l'Établissement", "Localisation du Marchand", "Référence Adresse", 
        "Secteur d'Activité", "Numéro du Marchand", "Identifiant du Marchand", "Montant de la Transaction"
    ]
    ws.append(header)

    # Ajouter les données des rapports
    for report in momopay_reports:
        row = [
            report.user.username,
            report.full_name,
            report.date_enregistrement,
            report.date_creation,
            report.heure_creation,
            report.nom_merchant,
            report.nom_etablissement,
            report.localisation_merchant,
            report.reference_adresse,
            report.secteur_activite,
            report.numero_merchant,
            report.identifiant_merchant,
            report.montant_transaction
        ]
        ws.append(row)

    # Créer une réponse HTTP avec un fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rapport_momopay.xlsx'

    # Sauvegarder le fichier Excel dans la réponse
    wb.save(response)
    return response

@login_required
def download_gsm_report(request):
    # Récupère les données à partir du modèle
    if request.user.has_perm('APP.view_all_gsm_reports'):
        gsm_reports = FormDataSupervisor.objects.all()  # Responsable GSM et DG voient tout
    else:
        gsm_reports = FormDataSupervisor.objects.filter(user=request.user)  # Utilisateur normal voit ses propres rapports

    # Créer un nouveau classeur Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rapport GSM"

    # Ajouter l'entête du tableau
    header = [
        "Utilisateur", "Nom Complet", "Date Enregistrement", "Lieu Activité", "Stock SIM Actives", 
        "Stock SIM Blanches", "SIM Appro", "Effectif Total", "Effectif Présent", "GSM", "Momo App",
        "MyMTN", "Ayoba", "Téléphone", "Modem", "MIFI", "WiFix", "Difficultés", "Momo Conversion", 
        "Reset PIN", "Prospection", "Besoin", "Concurrentielle"
    ]
    ws.append(header)

    # Ajouter les données des rapports
    for report in gsm_reports:
        row = [
            report.user.username,
            report.full_name,
            report.date_enregistrement,
            report.lieu_activite,
            report.stock_sim_activees,
            report.stock_sim_blanches,
            report.sim_appro,
            report.effectif_total,
            report.effectif_present,
            report.gsm,
            report.momo_app,
            report.mymtn,
            report.ayoba,
            report.telephone,
            report.modem,
            report.mifi,
            report.wifix,
            report.difficultes,
            report.momoconvertion,
            report.resetpin,
            report.prospection,
            report.besoin,
            report.concurrentielle
        ]
        ws.append(row)

    # Créer une réponse HTTP avec un fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rapport_gsm.xlsx'

    # Sauvegarder le fichier Excel dans la réponse
    wb.save(response)
    return response
