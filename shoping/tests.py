from django.test import TestCase
from .models import Customer, Product, Order, OrderItem

class CustomerCRUDTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com")

    def test_create_customer(self):
        customer = Customer.objects.create(name="New Customer", email="new@example.com")
        self.assertEqual(customer.name, "New Customer")

    def test_read_customer(self):
        customer = Customer.objects.get(id=self.customer.id)
        self.assertEqual(customer.name, "Test Customer")

    def test_update_customer(self):
        self.customer.name = "Updated Customer"
        self.customer.save()
        updated_customer = Customer.objects.get(id=self.customer.id)
        self.assertEqual(updated_customer.name, "Updated Customer")

    def test_delete_customer(self):
        self.customer.delete()
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())


class ProductCRUDTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100.00)

    def test_create_product(self):
        product = Product.objects.create(name="New Product", price=200.00)
        self.assertEqual(product.price, 200.00)

    def test_read_product(self):
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.name, "Test Product")

    def test_update_product(self):
        self.product.price = 150.00
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.price, 150.00)

    def test_delete_product(self):
        self.product.delete()
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


class OrderCRUDTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Order Customer", email="order@example.com")
        self.order = Order.objects.create(customer=self.customer)

    def test_create_order(self):
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(order.customer.name, "Order Customer")

    def test_read_order(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.customer, self.customer)

    def test_update_order(self):
        new_customer = Customer.objects.create(name="New Customer", email="newcustomer@example.com")
        self.order.customer = new_customer
        self.order.save()
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.customer, new_customer)

    def test_delete_order(self):
        self.order.delete()
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())


class OrderItemCRUDTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Item Customer", email="item@example.com")
        self.order = Order.objects.create(customer=self.customer)
        self.product = Product.objects.create(name="Item Product", price=100.00)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=5)
        self.assertEqual(order_item.quantity, 5)

    def test_read_order_item(self):
        order_item = OrderItem.objects.get(id=self.order_item.id)
        self.assertEqual(order_item.product.name, "Item Product")

    def test_update_order_item(self):
        self.order_item.quantity = 10
        self.order_item.save()
        updated_order_item = OrderItem.objects.get(id=self.order_item.id)
        self.assertEqual(updated_order_item.quantity, 10)

    def test_delete_order_item(self):
        self.order_item.delete()
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())
