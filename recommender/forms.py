from django import forms

class SignupForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(label="Password", max_length=30, required=True)
    dob = forms.DateField(required=True)
    gender = forms.CharField(required=True)
    image = forms.ImageField(required=False)
