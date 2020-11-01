import random

from django.shortcuts import render, redirect
from .models import *
from .helper import *
from .forms import *

def landing(request, username=None):
	context = {}
	context["username"] = username

	if username:
		context["logged_in"] = 1
	else:
		context["logged_in"] = 0

	if request.method == "GET":
		return render(request, "landing.html", context)

	else:
		return "In progress."

def login(request):
	context = {}
	context["logged_in"] = 0

	if request.method == "GET":
		login_form = LoginForm()
		context["form"] = login_form

		return render(request, "login.html", context)

	elif request.method == "POST":
		login_form = LoginForm(request.POST)

		if login_form.is_valid():
			login_info = login_form.cleaned_data
			valid_user = check_credentials(login_info=login_info)

			if valid_user:
				context["username"] = login_info["username"]
				return redirect('buyer_landing', username=login_info["username"])

		context["form"] = login_form
		context["error"] = 1
		return render(request, "login.html", context)


def sign_up(request):
	context = {}
	context["logged_in"] = 0

	if request.method == "GET":
		signup_form = SignUpForm()
		context["form"] = signup_form
		context["error"] = 0

		return render(request, "sign_up.html", context)

	elif request.method == "POST":
		signup_form = SignUpForm(request.POST)
		if signup_form.is_valid():
			signup_info = signup_form.cleaned_data

			error = create_user(signup_info=signup_info)

			if not error:
				return redirect('login')

			context["error"] = 1
			context["error_text"] = error
			context["form"] = signup_form

			return render(request, "sign_up.html", context)

def buyer_landing(request, username=None):
	context = {}
	context["username"] = username

	if username:
		context["logged_in"] = 1
	else:
		context["logged_in"] = 0

	if request.method == "GET":
		categories = get_all_product_categories()
		subset_categories = [category["category"] for category in categories]

		if username is not None:
			urls = ["/buyer_listing/" + username + "/" + category for category in subset_categories]
		else:
			urls = ["/buyer_listing/" + category for category in subset_categories]
		#image_paths = ["img/fruit.png", "img/shirt.jpg", "img/washing_machine.jpg"]
		image_paths = get_category_image(category_list=subset_categories)

		data = [{"category": subset_categories[i], "url": urls[i], "image_path": image_paths[i]} for i in range(len(urls))]

		context["data"] = data
		return render(request, "buyer_landing.html", context)

	else:
		return "In progress."


def buyer_listing(request, category, username=None):
	context = {}
	context["username"] = username

	if username:
		context["logged_in"] = 1
	else:
		context["logged_in"] = 0

	if request.method == "GET":
		listings = get_all_listings_by_category(category=category)
		context["listings"] = listings
		context["category"] = category
		return render(request, "buyer_listing.html", context)
	
	else:
		return "In progress."


def item_details(request, listing_id, username=None):
	context = {}
	context["username"] = username

	if username == "None":
		login_form = LoginForm()
		context["form"] = login_form

		return render(request, "login.html", context)

	context["logged_in"] = 1

	if request.method == "GET":
		listing = get_listing_details(listing_id=listing_id)
		context["listing"] = listing
		order_form = OrderForm()
		context["form"] = order_form

		return render(request, "item_details.html", context)

	else:
		order_form = OrderForm(request.POST)

		if order_form.is_valid():
			order_info = order_form.cleaned_data

			if order_info["order_quantity"] > 0:
				create_transaction(username=username,
								   listing_id=listing_id,
								   quantity=order_info["order_quantity"])

		return redirect('checkout', username=username)


def checkout(request, username):
	context={}
	context["username"] = username
	context["logged_in"] = 1

	if request.method == "GET":
		columns, data, subtotal = get_unpaid_transactions(username=username)
		context["columns"] = columns
		context["data"] = data
		context["subtotal"] = subtotal

		return render(request, "checkout.html", context)

	else:
		update_listings(username=username)

		return redirect('payment', username=username)


def payment(request, username):
	context = {}
	context["username"] = username
	context["logged_in"] = 1

	return render(request, "payment.html", context)
	






def seller_listing(request, username):
	context = {}
	context["username"] = username

	context["logged_in"] = 1

	if request.method == "GET":
		listings = get_all_seller_listings(username=username)
		context["listings"] = listings

		return render(request, "seller_listing.html", context)
	
	else:
		return "In progress."

def modify_item(request, username, listing_id):
	context = {}
	context["username"] = username
	context["logged_in"] = 1

	if request.method == "GET":
		listing = get_listing_details(listing_id=listing_id)

		data = {"item_name": listing["item_name"],
				"quantity": listing["quantity"],
				"expiration_date": listing["expiration_date"],
				"category": listing["category"]}

		i=1
		for tier in listing["price_tier_data"]:
			data["quantity_tier_{}".format(i)] = tier[1]
			data["price_tier_{}".format(i)] = tier[2]

			i += 1

		modify_form = ModifyForm(initial=data)

		context["listing"] = listing
		context["form"] = modify_form

		return render(request, "modify_item.html", context)

	else:
		form = ModifyForm(request.POST, request.FILES)

		if form.is_valid():
			form_data = form.cleaned_data

			create_modify_listing(username=username,
								  form=form_data,
								  listing_id=listing_id)

		return redirect("seller_listing", username=username)

def add_item(request, username):
	context = {}
	context["username"] = username
	context["logged_in"] = 1
	
	if request.method == "GET":
		modify_form = ModifyForm()

		context["form"] = modify_form

		return render(request, "add_item.html", context)

	else:
		form = ModifyForm(request.POST, request.FILES)

		if form.is_valid():
			form_data = form.cleaned_data

			create_modify_listing(username=username,
								  form=form_data)

		return redirect("seller_listing", username=username)