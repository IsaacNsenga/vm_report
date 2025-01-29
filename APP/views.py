from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FormDataSupervisor

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # On ne sauvegarde pas tout de suite pour ajouter des champs
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()  # Sauvegarde définitive
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

@login_required
def acceuil(request):
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

        telephone = request.POST.get('telephone')
        modem = request.POST.get('modem')
        mifi = request.POST.get('mifi')
        wifix = request.POST.get('wifix')

        difficultes = request.POST.get('difficultes')
        prospection = request.POST.get('prospection')
        besoin = request.POST.get('besoin')

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
            telephone=telephone,
            modem=modem,
            mifi=mifi,
            wifix=wifix,
            difficultes=difficultes,
            prospection=prospection,
            besoin=besoin
        )

        # Enregistrement des données dans la base de données
        form_data.save()

        # Message de succès
        message = "Formulaire soumis avec succès !"

    return render(request, 'acceuil.html', {'message': message})


def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def rapport(request):
    if request.user.is_superuser:
        reports = FormDataSupervisor.objects.all()
    else:
        reports = FormDataSupervisor.objects.filter(user=request.user)

    return render(request, 'rapport.html', {'reports': reports})
