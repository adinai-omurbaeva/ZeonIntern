from decimal import Decimal
from django.conf import settings
from mysite.models import Product, ProductImage

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, productimage, quantity=1, update_quantity=False):
        product_id = str(product.id)
        product_image_id = str(productimage.id)
        if product_id not in self.cart:
            self.cart[product_image_id] = {'quantity':0, 'price':str(product.price), 'old_price':str(product.old_price)}
        if update_quantity:
            self.cart[product_image_id]['quantity'] = quantity
        else:
            self.cart[product_image_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['old_price'] = item['old_price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
               self.cart.values())
               
    def get_old_price(self):
        return sum(Decimal(item['old_price']) * item['quantity'] for item in
               self.cart.values())

    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True