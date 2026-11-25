from django import forms
from .models import Client, Produit, Facture, LigneFacture, Paiement


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'telephone', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'stock']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'client', 'date_echeance', 'taux_tva']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: FAC-2026-001'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'date_echeance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['montant', 'mode', 'reference']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }
