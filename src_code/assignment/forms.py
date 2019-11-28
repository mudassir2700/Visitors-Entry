from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth import get_user_model
from .models  import Appointment



User=get_user_model()




class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email','name','role','department','sex','address',)



	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def check(self):
		if self.password1!=self.password2:
			print("passwords donot match")

	

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		#print(user)
		user.set_password(self.cleaned_data["password1"])

		ob = user.email
		ch=""
		msg=""
		ind1=ob.index('@')+1
		ind2 = len(ob)-4
		print(ob[ind1:ind2])

		#if ob[ind1:ind2]!='innov':
			#msg = 'Use your Companys Email Id'
			#return msg2
		if msg=="":
			if commit:
				user.active=True
				user.save()
		#user.save()
		return user,msg


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email','name','role','department','sex','address','password', 'active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]



class booking(forms.ModelForm):
	in_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
	out_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
	class Meta:
		model=Appointment
		fields=['name','email','contact','host']

class checkout_form(forms.ModelForm):
	booking_id = forms.IntegerField()
