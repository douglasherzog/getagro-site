from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "listing_type",
            "title",
            "description",
            "heads",
            "avg_weight_kg",
            "animal_category",
            "breed",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "heads": forms.NumberInput(attrs={"min": 1}),
            "avg_weight_kg": forms.NumberInput(attrs={"min": 1}),
        }
        labels = {
            "listing_type": "Tipo",
            "title": "Título",
            "description": "Descrição (opcional)",
            "heads": "Quantidade de cabeças (opcional)",
            "avg_weight_kg": "Peso médio (kg) (opcional)",
            "animal_category": "Categoria (opcional)",
            "breed": "Raça (opcional)",
        }
