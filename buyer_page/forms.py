from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=30,
                               widget=forms.TextInput(attrs={'name': 'username', 'placeholder': 'Username', 'class': 'pure-input-2-3',
                               								 'style': 'position: relative;'}))
    password = forms.CharField(label="password", max_length=30,
                               widget=forms.PasswordInput(attrs={'name': 'password', 'placeholder': 'Password', 'class': 'pure-input-2-3',
                               									 'style': 'position: relative;'}))
class OrderForm(forms.Form):
	order_quantity = forms.IntegerField(label="order_quantity", 
										widget=forms.TextInput(attrs={'name': 'order_quantity', 'value': 0, 'class': 'pure-input-1-3',
																	  'style': 'position: relative;'}))