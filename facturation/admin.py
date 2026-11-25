from django.contrib import admin

# Register your models here.

from .models import Client, Produit, Facture, LigneFacture, Paiement

admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Facture)
admin.site.register(LigneFacture)
admin.site.register(Paiement)
