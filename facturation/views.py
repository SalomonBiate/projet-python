from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Client, Produit, Facture
from .forms import (
    ClientForm,
    ProduitForm,
    FactureForm,
    LigneFactureForm,
    PaiementForm
)


def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client enregistré avec succès.")
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'facturation/client_form.html', {'form': form})


def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'facturation/liste_clients.html', {'clients': clients})


def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregistré avec succès.")
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'facturation/produit_form.html', {'form': form})


def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'facturation/liste_produits.html', {'produits': produits})


def ajouter_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save()
            messages.success(request, "Facture créée avec succès.")
            return redirect('detail_facture', facture_id=facture.id)
    else:
        form = FactureForm()
    return render(request, 'facturation/facture_form.html', {'form': form})


def liste_factures(request):
    factures = Facture.objects.select_related('client').all().order_by('-date_creation')
    return render(request, 'facturation/liste_factures.html', {'factures': factures})


def detail_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    ligne_form = LigneFactureForm()
    paiement_form = PaiementForm()
    return render(
        request,
        'facturation/detail_facture.html',
        {
            'facture': facture,
            'ligne_form': ligne_form,
            'paiement_form': paiement_form
        }
    )


def ajouter_ligne(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        form = LigneFactureForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data['produit']
            quantite = form.cleaned_data['quantite']

            if quantite <= 0:
                messages.error(request, "La quantité doit être supérieure à zéro.")
            elif produit.stock < quantite:
                messages.error(request, "Stock insuffisant pour ce produit.")
            else:
                with transaction.atomic():
                    ligne = form.save(commit=False)
                    ligne.facture = facture
                    ligne.prix_unitaire = produit.prix
                    ligne.save()

                    produit.stock -= quantite
                    produit.save()

                    if facture.statut == 'BROUILLON':
                        facture.statut = 'VALIDEE'
                        facture.save()

                messages.success(request, "Produit ajouté à la facture.")
    return redirect('detail_facture', facture_id=facture.id)


def ajouter_paiement(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            if montant <= 0:
                messages.error(request, "Le montant doit être supérieur à zéro.")
            elif montant > facture.reste_a_payer:
                messages.error(request, "Le montant dépasse le reste à payer.")
            else:
                with transaction.atomic():
                    paiement = form.save(commit=False)
                    paiement.facture = facture
                    paiement.save()

                    if facture.reste_a_payer <= 0:
                        facture.statut = 'PAYEE'
                        facture.save()

                messages.success(request, "Paiement enregistré avec succès.")
    return redirect('detail_facture', facture_id=facture.id)
