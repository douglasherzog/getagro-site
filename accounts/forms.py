from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import Profile


User = get_user_model()


class SignupForm(forms.Form):
    full_name = forms.CharField(label="Nome")
    document = forms.CharField(label="CPF/CNPJ")
    email = forms.EmailField(label="E-mail")
    phone = forms.CharField(label="Telefone/WhatsApp")
    address = forms.CharField(label="Endereço")
    city = forms.CharField(label="Cidade")
    state = forms.CharField(label="Estado", max_length=2)
    role = forms.ChoiceField(
        label="Tipo de conta",
        choices=[
            (Profile.ROLE_BUYER, "Comprador"),
            (Profile.ROLE_SELLER, "Vendedor"),
        ],
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

    def _normalize_document(self, raw: str) -> str:
        return "".join(ch for ch in (raw or "") if ch.isdigit())

    def _validate_cpf(self, cpf: str) -> bool:
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False
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
        return digits[9] == d1 and digits[10] == d2

    def _validate_cnpj(self, cnpj: str) -> bool:
        if len(cnpj) != 14:
            return False
        if cnpj == cnpj[0] * 14:
            return False
        digits = [int(d) for d in cnpj]

        def calc_digit(base_digits, weights):
            total = sum(d * w for d, w in zip(base_digits, weights))
            mod = total % 11
            return 0 if mod < 2 else 11 - mod

        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        w2 = [6] + w1
        d1 = calc_digit(digits[:12], w1)
        d2 = calc_digit(digits[:12] + [d1], w2)
        return digits[12] == d1 and digits[13] == d2

    def clean_document(self):
        raw = (self.cleaned_data["document"] or "").strip()
        doc = self._normalize_document(raw)

        if len(doc) not in (11, 14):
            raise forms.ValidationError("CPF/CNPJ inválido.")

        is_valid = self._validate_cpf(doc) if len(doc) == 11 else self._validate_cnpj(doc)
        if not is_valid:
            raise forms.ValidationError("CPF/CNPJ inválido.")

        return doc

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

        doc = cleaned.get("document")
        role = cleaned.get("role")
        if doc and role and p1 and not self.errors:
            user = User.objects.filter(username__iexact=doc).first()
            if user:
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    profile = None

                if profile and profile.role in (role, Profile.ROLE_BOTH):
                    self.add_error("document", "Este CPF/CNPJ já está cadastrado para este tipo. Faça login.")
                else:
                    authenticated_user = authenticate(username=doc, password=p1)
                    if authenticated_user is None:
                        self.add_error("password1", "Senha incorreta para este CPF/CNPJ.")

        return cleaned

    def save(self):
        doc = self.cleaned_data["document"]
        role = self.cleaned_data["role"]

        user = User.objects.filter(username__iexact=doc).first()
        if user is None:
            user = User.objects.create_user(
                username=doc,
                password=self.cleaned_data["password1"],
                email=self.cleaned_data["email"],
            )
            Profile.objects.create(
                user=user,
                role=role,
                full_name=self.cleaned_data["full_name"],
                document=doc,
                email=self.cleaned_data["email"],
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
                city=self.cleaned_data["city"],
                state=self.cleaned_data["state"],
            )
            return user

        user.email = self.cleaned_data["email"]
        user.save(update_fields=["email"])

        profile, _created = Profile.objects.get_or_create(
            user=user,
            defaults={
                "role": role,
                "full_name": self.cleaned_data["full_name"],
                "document": doc,
                "email": self.cleaned_data["email"],
                "phone": self.cleaned_data["phone"],
                "address": self.cleaned_data["address"],
                "city": self.cleaned_data["city"],
                "state": self.cleaned_data["state"],
            },
        )

        if profile.role != role and profile.role != Profile.ROLE_BOTH:
            profile.role = Profile.ROLE_BOTH

        profile.full_name = self.cleaned_data["full_name"]
        profile.email = self.cleaned_data["email"]
        profile.phone = self.cleaned_data["phone"]
        profile.address = self.cleaned_data["address"]
        profile.city = self.cleaned_data["city"]
        profile.state = self.cleaned_data["state"]
        profile.save()

        return user


class DocumentAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].label = "CPF/CNPJ"

    def clean_username(self):
        raw = (self.cleaned_data.get("username") or "").strip()
        return "".join(ch for ch in raw if ch.isdigit())
