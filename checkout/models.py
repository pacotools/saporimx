import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


# We'll use models.SET_NULL if the profile is deleted since that will allows
# us to keep an order history in the admin even if the user is deleted, and
# will also allow this to be either null or blank so that users who don't have
# an account can still make purchases. I'll add a related_name of orders so we
# can access the users orders by calling something like
# user.user.profile.orders

class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='País ', null=False, blank=False,
                           default='MX')
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                              default=0)
    tax2 = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                               default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                   default=0)
    observations = models.CharField(max_length=80, null=True, editable=True)
    delivery_type = models.CharField(max_length=10, null=True, editable=True)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def _generate_order_number(self):
        # Generate a random, unique order number using UUID
        return uuid.uuid4().hex.upper()

    def update_total(self):
        # Update grand total each time a line item is added,
        # accounting for delivery costs.

        # 'or 0' will prevent an error if we manually delete all the line items
        # from an order by making sure that this sets the order total to zero
        # instead of none
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            sdp = settings.STANDARD_DELIVERY_PERCENTAGE
            self.delivery_cost = self.order_total * sdp / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        # Override the original save method to set the order number
        # if it hasn't been set already.

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name="lineitems")
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2,
                                    null=True, blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                              default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                   default=0)
    observations = models.CharField(max_length=80, null=True, editable=True)

    def save(self, *args, **kwargs):
        # Override the original save method to set the lineitem total
        # and update the order total.

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
