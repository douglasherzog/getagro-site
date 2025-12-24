from django import forms

from .models import Lead, Procura


class ContactForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone",
            "message": "Mensagem",
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.interest = Lead.Interest.OTHER
        if commit:
            instance.save()
        return instance


class SellerLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "name",
            "email",
            "phone",
            "city_state",
            "heads",
            "avg_weight_kg",
            "animal_category",
            "breed",
            "timeframe",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "city_state": forms.TextInput(attrs={"placeholder": "Ex: Campo Grande/MS"}),
            "heads": forms.NumberInput(attrs={"min": 1}),
            "avg_weight_kg": forms.NumberInput(attrs={"min": 1}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone/WhatsApp",
            "city_state": "Cidade/UF",
            "heads": "Quantidade de cabeças",
            "avg_weight_kg": "Peso médio (kg)",
            "animal_category": "Categoria",
            "breed": "Raça (opcional)",
            "timeframe": "Prazo",
            "message": "Detalhes (opcional)",
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.interest = Lead.Interest.SELLER
        if commit:
            instance.save()
        return instance


class BuyerLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "name",
            "email",
            "phone",
            "city_state",
            "desired_volume",
            "specs",
            "timeframe",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "city_state": forms.TextInput(attrs={"placeholder": "Ex: Unidade: Goiânia/GO"}),
            "specs": forms.Textarea(attrs={"rows": 5}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone/WhatsApp",
            "city_state": "Cidade/UF",
            "desired_volume": "Volume desejado",
            "specs": "Especificações",
            "timeframe": "Janela de compra",
            "message": "Observações (opcional)",
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.interest = Lead.Interest.BUYER
        if commit:
            instance.save()
        return instance


class ProcuraForm(forms.ModelForm):
    class Meta:
        model = Procura
        fields = [
            "title",
            "city_state",
            "heads",
            "avg_weight_kg",
            "animal_category",
            "breed",
            "desired_volume",
            "timeframe",
            "specs",
        ]
        widgets = {
            "heads": forms.NumberInput(attrs={"min": 1}),
            "avg_weight_kg": forms.NumberInput(attrs={"min": 1}),
            "specs": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "title": "Título",
            "city_state": "Região (Cidade/UF)",
            "heads": "Quantidade de cabeças (opcional)",
            "avg_weight_kg": "Peso médio (kg) (opcional)",
            "animal_category": "Categoria (opcional)",
            "breed": "Raça (opcional)",
            "desired_volume": "Volume desejado (opcional)",
            "timeframe": "Janela/Prazo (opcional)",
            "specs": "Especificações (opcional)",
        }
