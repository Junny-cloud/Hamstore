from django import forms
from django.core.validators import RegexValidator
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *

class CommandesForm(forms.ModelForm): 
    ACTIONS = (
    ('valider', 'Validé'),
    ('rejeter', 'Réjeté')
    )
    etat_commande = forms.ChoiceField(choices=ACTIONS, label="Validation", widget=forms.Select(attrs={"class": "form-control", "id":"etat_commande", "placeholder":""}), required=True) 

    class Meta:
        model = Commandes
        fields = ['etat_commande', ]


    def clean_etat_commande(self):
        etat_commande = self.cleaned_data.get('etat_commande')
        if not etat_commande:
            raise forms.ValidationError('Ce champs est requis.')
        return etat_commande