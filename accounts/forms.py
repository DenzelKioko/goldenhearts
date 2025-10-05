from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form.
    Removes the 'role' field to prevent users from registering as admin.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserLoginForm(AuthenticationForm):
    """
    Custom login form that uses email instead of username and includes a 'Remember Me' checkbox.
    """
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'remember_me'}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')
        super().confirm_login_allowed(user)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['password'].widget.attrs['autocomplete'] = 'off'
        self.fields['remember_me'].label = "Remember Me"
        self.fields['remember_me'].label_attrs = {'class': 'form-check-label'}

# NEW: Profile Editing Form
class UserEditForm(forms.ModelForm):
    """
    Form for authenticated users to edit their profile details and picture.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})