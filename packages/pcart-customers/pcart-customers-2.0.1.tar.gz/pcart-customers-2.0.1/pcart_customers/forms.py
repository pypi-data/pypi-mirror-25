from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    PasswordResetForm,
    AuthenticationForm,
)
from .models import User, Customer


class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see '
            'this user\'s password, but you can change the password '
            'using <a href="password/">this form</a>.'))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        return self.initial['password']


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges,
    from the given email, phone and password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'duplicate_phone': _("A user with that phone already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            User.objects.get(phone=phone)
        except User.DoesNotExist:
            return phone
        raise forms.ValidationError(self.error_messages['duplicate_phone'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone')


class UserRegistrationForm(UserCreationForm):
    # accept_tos = forms.BooleanField(
    #     label=_(
    #         'I have read and accept the <a href="/terms/" '
    #         'rel="nofollow" target="_blank">Terms of Service</a>'),
    #     initial=False, required=False)

    class Meta:
        model = User
        fields = ('email', 'phone')

    # def clean_accept_tos(self):
    #     t = self.cleaned_data['accept_tos']
    #     if not t:
    #         raise forms.ValidationError(
    #             _('You should accept Terms of Service for registration.'))


class UserPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return (u for u in active_users)


class UserPasswordSetupForm(forms.Form):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2


class UserAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            'Please enter a correct email or phone and password. Note that both '
            'fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive'),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(UserAuthForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = _('Email or phone')


class UserPasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        help_text=_('Enter the email your account is registered for.')
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError(_('Unknown email.'))


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name',)
