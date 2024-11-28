from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

from django.contrib.auth.forms import SetPasswordForm


# Form to update the user information (This might be deleted or updated soon since I have two different pages for changing user information(UpdateUserForm)
# UpdateProfileForm() form changes user information but it makes sense to me to have all in the same page in the future.
class UpdateProfileForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telemóvel'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Endereço 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nº Porta/Andar/Apartamento'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cidade'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código Postal'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'País'}), required=False)
    
    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'zipcode', 'country')
    
# Form to Change the password.
class ChangePasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Palavra-chave'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>A tua palavra-passe não pode ser demasiado semelhante às tuas outras informações pessoais.</li>'
            '<li>A tua palavra-passe deve conter pelo menos 8 caracteres.</li>'
            '<li>A tua palavra-passe não pode ser uma palavra-passe habitualmente utilizada.</li>'
            '<li>A tua palavra-passe não pode ser inteiramente numérica.</li>'
            '</ul>'
        )

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar a tua palavra-chave.'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = (
            '<span class="form-text text-muted">'
            '<small>Introduza a mesma palavra-passe novamente.</small>'
            '</span>'
        )

class UpdateUserForm(UserChangeForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
	password = None
 
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nome do Utilizador'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>É necessário um nome de utilizador entre 10 a 20 letras e apenas é permitido os seguintes carateres: @/./+/-/_ </small></span>'

# Form to create an account for new users.
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nome do Utilizador'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>É necessário um nome de utilizador entre 10 a 20 letras e apenas é permitido os seguintes carateres: @/./+/-/_ </small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Palavra-chave'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>A tua palavra-passe não pode ser demasiado semelhante às tuas outras informações pessoais.</li><li> A tua palavra-passe deve conter pelo menos 8 caracteres.</li><li>A tua palavra-passe não pode ser uma palavra-passe habitualmente utilizada.</li><li>A tua palavra-passe não pode ser inteiramente numérica.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar a tua palavra-chave.'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Introduza a mesma palavra-passe novamente, para verificação.</small></span>'