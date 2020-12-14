from django import forms

class CadastroForm(forms.Form):
    email = forms.EmailField(label='Your name', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Primeiro Nome', max_length=100)
    last_name = forms.CharField(label='Último Nome', max_length=100)
    username = forms.CharField(label='Usuário', max_length=100)