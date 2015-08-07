from django import forms


class PasswordChangeForm(forms.Form):
	class Meta:
		old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña antigua'}))
		password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Nueva contraseña'}))
		password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repite nueva contraseña'}))
