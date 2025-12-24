from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField

from .models import Profile


User = get_user_model()


class SignupForm(forms.Form):
    username = UsernameField(
        label="Usuário",
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )
    full_name = forms.CharField(label="Nome")
    cpf = forms.CharField(label="CPF")
    address = forms.CharField(label="Endereço")
    city = forms.CharField(label="Cidade")
    state = forms.CharField(label="Estado", max_length=2)
    role = forms.ChoiceField(
        label="Tipo de conta",
        choices=Profile.ROLE_CHOICES,
        widget=forms.RadioSelect,
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este usuário já está em uso.")
        return username

    def clean_cpf(self):
        raw = (self.cleaned_data["cpf"] or "").strip()
        cpf = "".join(ch for ch in raw if ch.isdigit())

        if len(cpf) != 11:
            raise forms.ValidationError("CPF inválido.")

        if cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF inválido.")

        digits = [int(d) for d in cpf]

        def calc_digit(base_digits, factor_start):
            total = 0
            factor = factor_start
            for d in base_digits:
                total += d * factor
                factor -= 1
            mod = total % 11
            return 0 if mod < 2 else 11 - mod

        d1 = calc_digit(digits[:9], 10)
        d2 = calc_digit(digits[:9] + [d1], 11)

        if digits[9] != d1 or digits[10] != d2:
            raise forms.ValidationError("CPF inválido.")

        return cpf

    def clean_state(self):
        state = self.cleaned_data["state"].strip().upper()
        if len(state) != 2:
            raise forms.ValidationError("Informe o UF com 2 letras (ex.: RS).")
        return state

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")

        cpf = cleaned.get("cpf")
        role = cleaned.get("role")
        if cpf and role and not self.errors.get("cpf") and not self.errors.get("role"):
            if Profile.objects.filter(cpf=cpf, role=role).exists():
                self.add_error("cpf", "Este CPF já está cadastrado para este tipo de conta.")

        return cleaned

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password1"],
        )
        Profile.objects.create(
            user=user,
            role=self.cleaned_data["role"],
            full_name=self.cleaned_data["full_name"],
            cpf=self.cleaned_data["cpf"],
            address=self.cleaned_data["address"],
            city=self.cleaned_data["city"],
            state=self.cleaned_data["state"],
        )
        return user
