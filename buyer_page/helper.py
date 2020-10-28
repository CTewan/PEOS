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

	for transaction in unpaid_transactions:
		unit_price = float(transaction.unit_price)
		quantity = transaction.quantity
		seller = transaction.seller.username
		total_price = float(unit_price * quantity)

		listing = transaction.listing
		item_name = listing.item_name
		image_path = 1#listing.image_path
		orders_to_ship = max(0, listing.min_orders - listing.orders)

		data = [image_path, item_name, seller, unit_price, orders_to_ship, quantity, total_price]
		unpaid_transactions_data.append(data)

		subtotal += total_price

	return unpaid_transactions_columns, unpaid_transactions_data, subtotal

def delete_transaction(transaction):
    transaction = Transactions.objects.filter(pk=transaction.pk)
    listing = transaction.listing
    listing = Listing.objects.filter(pk=listing.pk)
    listing.update_orders(orders=-transaction.quantity)
    Transactions.objects.filter(pk=transaction.pk).delete()