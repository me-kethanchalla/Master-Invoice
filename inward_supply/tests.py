# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from .models import Supplier
# from django.db import IntegrityError

# class AddSupplierModelViewTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#         self.client.login(
#             username='testuser',
#             password='testpass123'
#         )
#         self.url = reverse('add_supplier')

#     def test_get_request_returns_form(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'inward_supply/add_supplier.html')
#         self.assertIn('form', response.context)
#         self.assertEqual(response.context.get('message', ''), '')

#     def test_post_valid_supplier_creates_supplier_and_redirects(self):
#         valid_data = {
#             'firm_name': 'Test Firm',
#             'person_name': 'Test Person',
#             'phone_number': '1234567890',
#             'email_id': 'supplier@example.com',
#             'address': '123 Test Street'
#         }
#         response = self.client.post(self.url, valid_data)
#         self.assertEqual(response.status_code, 302)
#         supplier_exists = Supplier.objects.filter(
#             email_id='supplier@example.com', user=self.user).exists()
#         self.assertTrue(supplier_exists)

#     def test_post_invalid_supplier_does_not_create_supplier(self):
#         invalid_data = {
#             'firm_name': '',  # Missing required value
#             'person_name': '',  # Missing required value
#             'phone_number': '1234567890',
#             'email_id': 'supplier@example.com',
#             'address': '123 Test Street'
#         }
#         response = self.client.post(self.url, invalid_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('form', response.context)
#         form = response.context['form']
#         self.assertTrue(form.errors)
#         print("Form Errors:", form.errors)
#         supplier_exists = Supplier.objects.filter(
#             email_id='supplier@example.com', user=self.user).exists()
#         self.assertFalse(supplier_exists)

#     def test_unique_firm_name_per_user(self):
#         # Create a supplier with a specific firm name.
#         supplier1 = Supplier.objects.create(
#             user=self.user,
#             firm_name='Test Firm',
#             person_name= 'Test Person',
#             phone_number= '1234567890',
#             email_id= 'supplier@example.com',
#             address= '123 Test Street'
#         )
#         #Attempt to create another supplier with the same firm name.
#         with self.assertRaises(IntegrityError):
#             Supplier.objects.create(
#                 user=self.user,
#                 firm_name='Test Firm',
#                 person_name= 'Test Person',
#                 phone_number= '1234567890',
#                 email_id= 'supplier@example.com',
#                 address= '123 Test Street'
#             )

# class viewSuppliersTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser', 
#             password='testpass123'
#         )
#         self.client.login(username='testuser', password='testpass123')
#         self.supplier1 = Supplier.objects.create(
#             user=self.user, firm_name="Test Firm 1",
#             person_name="Test Person 1", 
#             phone_number="1234567890",
#             email_id="supplier1@example.com", 
#             address="123 Test Street",
#             debit=100.0, total_sales=5000.0
#         )
#         self.supplier2 = Supplier.objects.create(
#             user=self.user, firm_name="Test Firm 2",
#             person_name="Test Person 2", 
#             phone_number="0987654321",
#             email_id="supplier2@example.com", 
#             address="456 Sample Road",
#             debit=200.0, total_sales=10000.0
#         )

#     def test_view_suppliers_list(self):
#         response = self.client.get(reverse('view_suppliers'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'inward_supply/view_suppliers.html')
#         self.assertContains(response, "Test Firm 1")
#         self.assertContains(response, "Test Firm 2")

#     def test_search_suppliers_by_firm_name(self):
#         response = self.client.get(reverse('view_suppliers'), {'query': 'Test Firm 1'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Firm 1")
#         self.assertNotContains(response, "Test Firm 2")

#     def test_search_suppliers_by_person_name(self):
#         response = self.client.get(reverse('view_suppliers'), {'query': 'Test Person 2'})
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Firm 2")
#         self.assertNotContains(response, "Test Firm 1")

#     def test_edit_supplier(self):
#         edit_url = reverse('edit_supplier', args=[self.supplier1.id])
#         updated_data = {
#             'firm_name': 'Updated Firm',
#             'person_name': 'Updated Person',
#             'phone_number': '9999999999',
#             'email_id': 'updated@example.com',
#             'address': '789 New Street'
#         }
#         response = self.client.post(edit_url, updated_data)
#         self.assertEqual(response.status_code, 302)                         # Redirects to view_suppliers
#         self.supplier1.refresh_from_db()
#         self.assertEqual(self.supplier1.firm_name, 'Updated Firm')
#         self.assertEqual(self.supplier1.person_name, 'Updated Person')
#         self.assertEqual(self.supplier1.phone_number, '9999999999')
#         self.assertEqual(self.supplier1.email_id, 'updated@example.com')
#         self.assertEqual(self.supplier1.address, '789 New Street')
#         #Ensure debit and total_sales remain unchanged
#         self.assertEqual(self.supplier1.debit, 100.0)
#         self.assertEqual(self.supplier1.total_sales, 5000.0)

#     def test_delete_supplier(self):
#         """Test deleting a supplier."""
#         delete_url = reverse('delete_supplier', args=[self.supplier1.id])
#         response = self.client.post(delete_url) 
#         self.assertEqual(response.status_code, 302)
#         self.assertFalse(Supplier.objects.filter(id=self.supplier1.id).exists())

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import json

from inward_supply.models import Supplier, InvoiceBill,ProductEntry
from inventory.models import Inventory
from django.db import IntegrityError

class AddInvoiceTest(TestCase):
    def setUp(self):
        """Set up a test user, supplier, and two inventory products."""
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.supplier = Supplier.objects.create(
            user=self.user,firm_name="Test Supplier",
            person_name="Supplier Person",phone_number="1234567890",
            email_id="supplier@example.com",
            address="123 Test Street",
        )
        self.inventory_product1 = Inventory.objects.create(
            user=self.user, item_id="P001", 
            product_name="Test Product 1", quantity=10,
            cost_price=Decimal('100.00'), sale_price=Decimal('150.00'),
            max_retail_price=Decimal('200.00'), gst=Decimal('10.00'),
        )
        self.inventory_product2 = Inventory.objects.create(
            user=self.user, item_id="P002", 
            product_name="Test Product 2", quantity=20, 
            cost_price=Decimal('200.00'), sale_price=Decimal('250.00'),
            max_retail_price=Decimal('300.00'), gst=Decimal('5.00'),
        )
    
    def test_get_add_invoice_page(self):
        url = reverse('add-inward-bill')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inward_supply/invoice_form.html")

    def test_post_valid_invoice_creates_invoice_and_product_entries(self):
        url = reverse('add-inward-bill')
        data = {
            'bill_number': 'INV001', 'date': '2025-04-03',
            'billed-to': str(self.supplier.id),
            'product_id[]': [str(self.inventory_product1.id), str(self.inventory_product2.id)],
            'quantity[]': ['5', '3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('invoice_list'))

        invoice = InvoiceBill.objects.filter(user=self.user, bill_number='INV001').first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.supplier, self.supplier)
        product_entries = ProductEntry.objects.filter(invoice=invoice)
        self.assertEqual(product_entries.count(), 2)

        expected_amount1 = ((self.inventory_product1.cost_price*Decimal(5))*
                            (1 + (self.inventory_product1.gst / Decimal(100))))
        expected_amount2 = ((self.inventory_product2.cost_price *Decimal(3))*
                            (1 + (self.inventory_product2.gst / Decimal(100))))

        pe1 = product_entries.filter(product_name=self.inventory_product1.product_name).first()
        self.assertIsNotNone(pe1)
        self.assertEqual(pe1.quantity, 5)
        self.assertEqual(Decimal(pe1.amount), expected_amount1)

        pe2 = product_entries.filter(product_name=self.inventory_product2.product_name).first()
        self.assertIsNotNone(pe2)
        self.assertEqual(pe2.quantity, 3)
        self.assertEqual(Decimal(pe2.amount), expected_amount2)

        total_invoice_amount = expected_amount1 + expected_amount2
        self.assertEqual(Decimal(invoice.get_total_amount()), total_invoice_amount)

    def test_post_duplicate_bill_number_shows_error(self):
        url = reverse('add-inward-bill')
        InvoiceBill.objects.create(user=self.user, bill_number='INV002', date='2025-04-03')
        data = {
            'bill_number': 'INV002',
            'date': '2025-04-03',
            'product_id[]': [str(self.inventory_product1.id)],
            'quantity[]': ['3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bill number already exists")

    def test_post_invoice_missing_required_field_shows_error(self):
        url = reverse('add-inward-bill')
        data = {
        # 'bill_number' is intentionally omitted
        'date': '2025-04-03',
        'billed-to': str(self.supplier.id),
        'product_id[]': [str(self.inventory_product1.id), str(self.inventory_product2.id)],
        'quantity[]': ['5', '3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required", msg_prefix="Missing bill number should trigger an error")

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from inward_supply.models import Supplier, InvoiceBill, ProductEntry
from inventory.models import Inventory
from datetime import date

class InwardInvoiceViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        self.supplier = Supplier.objects.create(
            user=self.user,firm_name='Test Supplier',
            person_name='Alice', phone_number='1234567890',
            email_id='alice@gmail.com',address='123 Main St'
        )
        self.invoice1 = InvoiceBill.objects.create(
            user=self.user,
            date='2025-04-03',
            bill_number='INV100',
            supplier=self.supplier,
        )
        self.invoice2 = InvoiceBill.objects.create(
            user=self.user,
            date='2025-04-04',
            bill_number='INV200',
            supplier=self.supplier,
        )
        ProductEntry.objects.create(invoice=self.invoice1, product_name='Product A', quantity=4, amount=40.0)
        ProductEntry.objects.create(invoice=self.invoice1, product_name='Product B', quantity=2, amount=30.0)
        ProductEntry.objects.create( invoice=self.invoice2, product_name='Product C', quantity=5, amount=75.0)

    def test_invoice_list_shows_all_user_invoices(self):
        url = reverse('invoice_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inward_supply/view_bill.html")

        self.assertContains(response, 'INV100')
        self.assertContains(response, 'INV200')
        self.assertContains(response, self.supplier.firm_name)

    def test_invoice_detail_shows_correct_invoice_and_products(self):
        url = reverse('invoice_detail', args=[self.invoice1.bill_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inward_supply/invoice_detail.html")

        self.assertContains(response, self.invoice1.bill_number)
        self.assertContains(response, self.supplier.firm_name)

        self.assertContains(response, 'Product A')
        self.assertContains(response, 'Product B')
        self.assertNotContains(response, 'Product C')
