import random

from django.shortcuts import render, redirect
from .models import *
from .helper import *
from .forms import *

def login(request):
	context = {}

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




# Create your views here.
def buyer_landing(request, username=None):
	context = {}
	context["username"] = username

	if request.method == "GET":
		categories = get_all_product_categories()
		subset_categories = random.choices(categories, k=3)
		subset_categories = [category["category"] for category in subset_categories]

		if username is not None:
			urls = ["/buyer_listing/" + username + "/" + category for category in subset_categories]
		else:
			urls = ["/buyer_listing/" + category for category in subset_categories]
		image_paths = ["img/fruit.png", "img/shirt.jpg", "img/washing_machine.jpg"] 

		data = [{"category": subset_categories[i], "url": urls[i], "image_path": image_paths[i]} for i in range(len(urls))]

		context["data"] = data
		return render(request, "buyer_landing.html", context)

	else:
		return "In progress."


def buyer_listing(request, category, username=None):
	context = {}
	context["username"] = username

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

	if request.method == "GET":
		listing = get_listing_details(listing_id=listing_id)
		context["listing"] = listing
		order_form = OrderForm()
		context["form"] = order_form

		return render(request, "item_details.html", context)

	
