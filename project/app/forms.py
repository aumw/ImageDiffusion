from django import forms
from .models import Prompt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PromptForm(forms.ModelForm):
	prompt = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder":"Prompt", "class":"form-control", "rows":3}), label="",)
	original_image = forms.ImageField(label="Image")

	class Meta:
		model = Prompt
		exclude = ("user", "diffused_image")


class SignUpForm(UserCreationForm):
	# email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class":"form-control"}))
	# first_name = forms.EmailField(label="First Name", max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
	# last_name = forms.EmailField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].label = 'Username'
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].label = 'Password'
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].label = 'Confirm Password'
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
