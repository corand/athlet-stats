from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserProfileCreationForm(forms.ModelForm):
	password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ("email","profile_picture","name","first_surname","second_surname","gender","self_description_es","self_description_eu","coach_description")

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			msg = "Passwords don't match"
			raise forms.ValidationError(msg)
		return password2

	def save(self,commit=True):
		user = super(UserProfileCreationForm,self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserProfileChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = UserProfile

	def clean_password(self):
		return self.initial['password']



class UserProfileAdmin(UserAdmin):
	add_form = UserProfileCreationForm
	form = UserProfileChangeForm

	list_display = ("email","is_staff","profile_picture","name","first_surname","second_surname","gender","self_description_es","self_description_eu","coach_description")
	list_filter = ("is_staff","is_superuser","is_active","groups")
	search_fields = ("email","name","first_surname")
	ordering = ("email",)
	filter_horizontal = ("groups","user_permissions",)
	fieldsets = (
			(None, {"fields": ("email","password")}),
			("Personal info", {"fields":
										("name","first_surname","second_surname","profile_picture","gender","self_description_es","self_description_eu","coach_description")}),
			("Permissions", {"fields": ("is_active", "is_staff","is_superuser","groups","user_permissions")}),
			("Important dates", {"fields":("last_login",)}),
		)
	add_fieldsets = ((None, { "classes": ("wide",), "fields": ("email","name","first_surname","second_surname","self_description_es","self_description_eu","coach_description","password1","password2")}),)


admin.site.register(UserProfile,UserProfileAdmin)