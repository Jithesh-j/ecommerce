from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, SetPasswordForm
from django import forms
from .models import Customer_Profile

# Update Password
class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2') 

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label, 'label': '', 'help_text': field.help_text})


# Register 
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="E-mail 📧", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
          
		def __init__(self, *args, **kwargs):
			super(SignUpForm, self).__init__(*args, **kwargs)

			for field in self.fields.values():
				field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label, 'label': '', 'help_text': field.help_text})


# Update User Details
class UpdateUserForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="E-mail 📧", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),required=False)
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),required=False)
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),required=False)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label, 'label': '', 'help_text': field.help_text})

# Update Personal Profile Details
class UpdateProfileInfo(forms.ModelForm):
    phone = forms.CharField(label="Phone number", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}), required=True)
    address = forms.CharField(label="Address", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),required=True)
    city = forms.CharField(label="City", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'city'}),required=True)
    state = forms.CharField(label="State", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),required=True)
    zipcode = forms.CharField(label="Zip-Code", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zipcode'}),required=True)
    country = forms.CharField(label="Country", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),required=True)

    class Meta: 
         model = Customer_Profile 
         fields = ('phone', 'address', 'city', 'state', 'zipcode', 'country')
