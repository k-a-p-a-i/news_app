from django import forms
from django.core.validators import MinLengthValidator

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Account

class ContactForm(forms.Form):
	#форма обратной связи

    name = forms.CharField(max_length=40,label='Имя пользователя', validators= [MinLengthValidator(2)])
    email = forms.EmailField(label='Email')
    message = forms.CharField(max_length=100, label='Введите сообщение',
                              widget=forms.Textarea)



def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise forms.ValidationError("Такой адрес электронный почты уже используется!")



class UserForm(UserCreationForm):
	# форма регистрации нового пользователя
	username = forms.CharField(label="Логин")
	email = forms.EmailField(required=True, validators = [validate_email])
	password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', "password1", "password2")

		def save(self, commit=True):
			user = super(UserForm, self).save(commit=False)
			user.email = self.cleaned_data['email']
			if commit:
				user.save()
			return user



class ProfileForm(forms.ModelForm):
	#форма обновления данных профиля
	class Meta:
		model = Account
		fields = ('birthdate', 'gender', 'account_image')
		widgets = {
			'birthdate': forms.DateInput(
				attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
			)
		}

class UserUpdateForm(UserChangeForm):
	# форма обновления данных класса User
	password = None
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', )


