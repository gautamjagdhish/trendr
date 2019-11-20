from django import forms
from .models import Tweet, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TweetCreateForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ('title','content','hashtag')


class TweetEditForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ('title','content','hashtag')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob','photo']



class UserLoginForm(forms.ModelForm):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username','password')


# class UserRegistrationForm(forms.ModelForm):
# 	password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Enter Password Here...'}))
# 	confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder' : 'Confirm Password...'}))
# 	class Meta:
# 		model = User
# 		fields = (
# 			'username',
# 			'first_name',
# 			'last_name',
# 			'email',
# 			)

# 	def clean_confirm_password(self):
# 		password = self.cleaned_data.get('password')
# 		confirm_password = self.cleaned_data.get('confirm_password')
# 		if password != confirm_password:
# 			raise forms.ValidationError("Password Mismatch")
# 		return confirm_password

class UserEditForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	#email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('user',)