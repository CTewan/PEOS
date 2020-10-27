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