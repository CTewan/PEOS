from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=30,
                               widget=forms.TextInput(attrs={'name': 'username', 'placeholder': 'Username', 'class': 'pure-input-2-3',
                               								 'style': 'position: relative;'}))
    password = forms.CharField(label="password", max_length=30,
                               widget=forms.PasswordInput(attrs={'name': 'password', 'placeholder': 'Password', 'class': 'pure-input-2-3',
                               									 'style': 'position: relative;'}))

class SignUpForm(forms.Form):
    username = forms.CharField(label="username", max_length=30,
                               widget=forms.TextInput(attrs={'name': 'username', 'class': 'pure-input-1-2',
                               								 'style': 'position: relative;'}))
    password = forms.CharField(label="password", max_length=30,
                               widget=forms.PasswordInput(attrs={'name': 'password', 'class': 'pure-input-1-2',
                               									 'style': 'position: relative;'}))
    first_name = forms.CharField(label="first_name", max_length=30,
                                 widget=forms.TextInput(attrs={'name': 'first_name', 'placeholder': 'Given name', 'class': 'pure-input-1-2',
                               								   'style': 'position: relative;'}))

    last_name = forms.CharField(label="last_name", max_length=30,
                                widget=forms.TextInput(attrs={'name': 'last_name', 'placeholder': 'Family name', 'class': 'pure-input-1-2',
                               								  'style': 'position: relative;'}))

    email = forms.EmailField(label="email", max_length=50,
    						 widget=forms.TextInput(attrs={'name': 'email', 'class': 'pure-input-3-4',
    						 							   'style': 'position: relative;'}))

    delivery_address = forms.CharField(label="delivery_address", max_length=100,
		                               widget=forms.TextInput(attrs={'name': 'delivery_address', 'class': 'pure-input-3-4',
		                               								 'style': 'position: relative;'}))

    billing_address = forms.CharField(label="billing_address", max_length=100,
		                               widget=forms.TextInput(attrs={'name': 'mailing_address', 'class': 'pure-input-3-4',
		                               								 'style': 'position: relative;'}))


class OrderForm(forms.Form):
	order_quantity = forms.IntegerField(label="order_quantity", 
										widget=forms.TextInput(attrs={'name': 'order_quantity', 'value': 0, 'class': 'pure-input-1-3',
																	  'style': 'position: relative;'}))

class ModifyForm(forms.Form):
	item_name = forms.CharField(label="item_name", max_length=200,
								widget=forms.TextInput(attrs={'name': 'item_name', 'class': 'pure-input-3-4',
															  'style': 'position: relative;'}))

	quantity = forms.IntegerField(label="quantity", 
								  widget=forms.TextInput(attrs={'name': 'quantity', 'class': 'pure-input-1-2',
															   'style': 'position: relative;'}))

	expiration_date = forms.DateTimeField(label="expiration_date",
										  widget=forms.DateTimeInput(attrs={'name': 'expiration_date', 'class': 'pure-input-1-4',
										  									'style': 'position: relative;'}))

	category = forms.CharField(label='category', max_length=200,
							   widget=forms.TextInput(attrs={'name': 'item_name', 'class': 'pure-input-1-2',
															  'style': 'position: relative;'}))

	quantity_tier_1 = forms.IntegerField(label="quantity_tier_1", 
										 required=True,
								  		 widget=forms.TextInput(attrs={'name': 'quantity_tier_1', 'class': 'pure-input-1-2',
															   		   'style': 'position: relative;'}))

	quantity_tier_2 = forms.IntegerField(label="quantity_tier_2", 
										 required=False,
								  		 widget=forms.TextInput(attrs={'name': 'quantity_tier_2', 'class': 'pure-input-1-2',
															   		   'style': 'position: relative;'}))

	quantity_tier_3 = forms.IntegerField(label="quantity_tier_3", 
										 required=False,
								  		 widget=forms.TextInput(attrs={'name': 'quantity_tier_3', 'class': 'pure-input-1-2',
															   		   'style': 'position: relative;'}))

	price_tier_1 = forms.DecimalField(label='price_tier_1',
									  max_digits=9,
									  decimal_places=2,
									  required=True,
									  widget=forms.TextInput(attrs={'name': 'price_tier_1', 'class': 'pure-input-1-2',
															   		'style': 'position: relative;'}))

	price_tier_2 = forms.DecimalField(label='price_tier_2',
									  max_digits=9,
									  decimal_places=2,
									  required=False,
									  widget=forms.TextInput(attrs={'name': 'price_tier_2', 'class': 'pure-input-1-2',
															   		'style': 'position: relative;'}))

	price_tier_3 = forms.DecimalField(label='price_tier_3',
									  max_digits=9,
									  decimal_places=2,
									  required=False,
									  widget=forms.TextInput(attrs={'name': 'price_tier_3', 'class': 'pure-input-1-2',
															   		'style': 'position: relative;'}))

	image = forms.ImageField(label='image',
							 required=False,
							 widget=forms.ClearableFileInput())