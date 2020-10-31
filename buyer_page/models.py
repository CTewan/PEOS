from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.
class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    userid = models.AutoField(primary_key=True, default=None)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=100, null=True, default=None, blank=True)
    billing_address = models.CharField(max_length=100, null=True, default=None, blank=True)

    def get_username(self):
        return self.username

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_historical_purchases(self):
        historical_purchases = self.buyer.get_historical_purchases()

        return historical_purchases

    def get_pending_purchases(self):
        pending_purchases = self.buyer.get_pending_purchases()
        
        return pending_purchases

    def get_active_listings(self):
        active_listings = self.seller.get_active_listings()

        return active_listings

    def get_all_listings(self):
        all_listings = self.seller.get_listings()

        return all_listings



class Buyer(User):
    user_ptr = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    parent_link=True,
                                    primary_key=True,
                                    default=None)

    def get_historical_purchases(self):
        return Transactions.objects.filter(seller=self, completed=True)

    def get_pending_purchases(self):
        return Transactions.objects.filter(seller=self, completed=False)

class Seller(User):
    user_ptr = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    parent_link=True,
                                    primary_key=True,
                                    default=None)

    def get_listings(self):
        return Listing.objects.filter(seller=self)

    def get_active_listings(self):
        return Listing.objects.filter(seller=self, active=True)

class Listing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    listing_id = models.AutoField(primary_key=True, default=None)
    item_name = models.CharField(max_length=200)
    unit_price = models.JSONField(null=False)
    quantity = models.IntegerField(null=False)
    orders = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(default=None)
    image_path_s = models.CharField(max_length=200, null=True, default=None)
    image_path_l = models.CharField(max_length=200, null=True, default=None)
    active = models.BooleanField(default=False)
    category = models.CharField(max_length=200, default=None, null=True)
    min_orders = models.IntegerField(default=0)
    current_price =  models.DecimalField(max_digits=9, decimal_places=2, default=0)


    def update_orders(self, orders):
        self.orders += orders
        self.orders = max(0, self.orders)
        self.save()

    def get_current_price(self):
        prices = [(int(k), float(v)) for k, v in self.unit_price.items()]
        prices = sorted(prices, key=lambda x: x[0])

        quant_tier = prices[0][0]
        curr_price = prices[0][1]

        for i in range(len(prices)):
            quant = prices[i][0]
            price = prices[i][1]

            if self.orders >= quant:
                quant_tier = quant
                curr_price = price
                
        self.current_price = curr_price
        self.save()

        return curr_price

    def get_min_orders(self):
        self.min_orders = min(self.unit_price.keys())
        self.save()

    def process_unit_price(self):
        i = 1
        data = []
        for quantity, price in self.unit_price.items():
            data.append([i, int(quantity), round(float(price),2)])
            i += 1

        return data

    def update_all_transactions(self):
        transactions = Transactions.objects.filter(listing=self)
        current_price = self.get_current_price()

        if len(transactions) > 0:
            for transaction in transactions:
                transaction.unit_price = current_price
                transaction.save()


class Transactions(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_number = models.AutoField(primary_key=True, default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)

    unit_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def completed_transaction(self):
        self.completed = True
        self.save()

    def update_listing_orders(self):
        self.listing.update_orders(orders=self.quantity)

    def update_unit_price(self):
        transaction_set = Transactions.objects.filter(listing=self.listing)
        unit_price = self.listing.get_current_price()
        for transaction in transaction_set:
            transaction.unit_price = unit_price

        Transactions.objects.bulk_update(transaction_set, ["unit_price"])





