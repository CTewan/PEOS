import os
from pathlib import Path
import random

from PIL import Image

from .models import *

def delete_transaction(transaction):
    transaction = Transactions.objects.filter(pk=transaction.pk)
    listing = transaction.listing
    listing = Listing.objects.filter(pk=listing.pk)
    listing.update_orders(orders=-transaction.quantity)
    models.Transactions.objects.filter(pk=transaction.pk).delete()

def get_all_product_categories():
    categories = Listing.objects.filter(active=True).order_by().values('category').distinct()

    return categories

def get_category_image(category_list):
	image_paths = []

	for category in category_list:
		listings = Listing.objects.filter(category=category, active=True)
		listing = random.choice(listings)
		image = listing.image_path_l
		image_paths.append(image)

	return image_paths

def create_user(signup_info):
	user = User()

	existing_username = len(User.objects.filter(username=signup_info["username"])) > 0
	existing_email = len(User.objects.filter(email=signup_info["email"])) > 0

	error_text = []

	if existing_username:
		error_text.append("Username {}".format(signup_info["username"]))

	if existing_email:
		error_text.append("Email {}".format(signup_info["email"]))

	if len(error_text) > 0:
		error_text = " and ".join(error_text)
		error_text += " already exists."

		return error_text

	user.first_name = signup_info["first_name"]
	user.last_name = signup_info["last_name"]
	user.username = signup_info["username"]
	user.email = signup_info["email"]
	user.password = signup_info["password"]
	user.delivery_address = signup_info["delivery_address"]
	user.billing_address = signup_info["billing_address"]

	user.save()

	buyer = Buyer(user_ptr=user)
	buyer.__dict__.update(user.__dict__)
	buyer.save()

	seller = Seller(user_ptr=user)
	seller.__dict__.update(user.__dict__)
	seller.save()

	return False

def check_credentials(login_info):
	username = login_info["username"]
	password = login_info["password"]

	user = User.objects.filter(username=username, password=password)
	if len(user) < 1:
		return False

	return True

def get_all_listings_by_category(category):
	listings = Listing.objects.filter(category=category, active=True).values()


	for listing in listings:
		seller = listing["seller_id"]
		seller = Seller.objects.get(pk=seller)
		seller = seller.username

		listing["seller_name"] = seller

	return listings

def get_listing_details(listing_id):
	listing = Listing.objects.get(listing_id=listing_id)
	price_tier_data = listing.process_unit_price()
	listing = listing.__dict__

	seller = listing["seller_id"]
	seller = Seller.objects.get(pk=seller)
	seller = seller.username

	listing["seller_name"] = seller
	listing["price_tier_data"] = price_tier_data
	listing["price_tier_columns"] = ["Tier", "Quantity", "Price"]

	return listing

def create_transaction(username, listing_id, quantity):
	buyer = User.objects.get(username=username).buyer
	listing = Listing.objects.get(listing_id=listing_id)
	seller = listing.seller

	transaction = Transactions(listing=listing, buyer=buyer, seller=seller, quantity=quantity)
	transaction.save()
	transaction.update_unit_price()

def update_listings(username):
	buyer = User.objects.get(username=username).buyer
	unpaid_transactions = Transactions.objects.filter(buyer=buyer, completed=False)

	for transaction in unpaid_transactions:
		transaction.update_listing_orders()
		transaction.update_unit_price()
		transaction.completed = True
		transaction.save()

def get_unpaid_transactions(username):
	buyer = User.objects.get(username=username).buyer
	unpaid_transactions = Transactions.objects.filter(buyer=buyer, completed=False)

	unpaid_transactions_data = []
	unpaid_transactions_columns = ["", "Product Name", "Seller", "Unit Price", "Orders to Ship", "Quantity Ordered", "Total Price"]
	subtotal = 0

	i = 1

	for transaction in unpaid_transactions:
		unit_price = float(transaction.unit_price)
		quantity = transaction.quantity
		seller = transaction.seller.username
		total_price = float(unit_price * quantity)

		listing = transaction.listing
		item_name = listing.item_name
		image_path = i
		orders_to_ship = max(0, listing.min_orders - listing.orders)

		data = [image_path, item_name, seller, unit_price, orders_to_ship, quantity, total_price]
		unpaid_transactions_data.append(data)

		subtotal += total_price
		i += 1

	return unpaid_transactions_columns, unpaid_transactions_data, subtotal

def delete_transaction(transaction):
    transaction = Transactions.objects.filter(pk=transaction.pk)
    listing = transaction.listing
    listing = Listing.objects.filter(pk=listing.pk)
    listing.update_orders(orders=-transaction.quantity)
    Transactions.objects.filter(pk=transaction.pk).delete()


def get_all_seller_listings(username):
	seller = User.objects.get(username=username).seller

	listings = seller.get_active_listings()
	listings = listings.values()

	return listings

def _process_image(img_obj, listing_id):
	LARGE_SIZE = (200, 200)
	SMALL_SIZE = (50, 50)

	img = Image.open(img_obj)

	if img.mode in ("RGBA", "P"): 
		img = img.convert("RGB")

	large_img = img.resize(LARGE_SIZE)
	small_img = img.resize(SMALL_SIZE)

	large_img.save(os.path.join(Path(__file__).resolve().parent, "static", "img", str(listing_id) + "L.jpg"))
	small_img.save(os.path.join(Path(__file__).resolve().parent, "static", "img", str(listing_id) + "S.jpg"))


def create_modify_listing(username, form, listing_id=None):
	seller = User.objects.get(username=username).seller

	if listing_id:
		listing = Listing.objects.get(listing_id=listing_id)

		if listing.seller != seller:
			return False
	else:
		listing = Listing()
		listing.seller = seller

	listing.quantity = form["quantity"]
	listing.item_name = form["item_name"]
	listing.expiration_date = form["expiration_date"]
	listing.category = form["category"]

	unit_price = {}
	unit_price[form["quantity_tier_1"]] = float(form["price_tier_1"])

	if form["quantity_tier_2"] and form["price_tier_2"]:
		unit_price[form["quantity_tier_2"]] = float(form["price_tier_2"])

	if form["quantity_tier_3"] and form["price_tier_3"]:
		unit_price[form["quantity_tier_3"]] = float(form["price_tier_3"])

	listing.unit_price = unit_price
	listing.active = True
	listing.save()
	listing.get_min_orders()

	listing_id = listing.listing_id

	if form["image"]:
		image = form["image"]
		_process_image(img_obj=image, listing_id=listing_id)

		listing.image_path_s = "/static/img/" + str(listing_id) + "S.jpg"
		listing.image_path_l = "/static/img/" + str(listing_id) + "L.jpg"

	listing.save()
	listing.update_all_transactions()