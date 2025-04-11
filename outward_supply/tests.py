from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Retailer
from django.db import IntegrityError

class AddRetailerModelViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.url = reverse('add_retailer')

    def test_get_request_returns_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'outward_supply/add_retailer.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context.get('message', ''), '')

    def test_post_valid_retailer_creates_retailer_and_redirects(self):
        valid_data = {
            'firm_name': 'Test Retailer',
            'person_name': 'Retailer Person',
            'phone_number': '1234567890',
            'email_id': 'retailer@example.com',
            'address': '456 Retail Street'
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 200)
        retailer_exists = Retailer.objects.filter(
            email_id='retailer@example.com', user=self.user).exists()
        self.assertTrue(retailer_exists)

    def test_post_invalid_retailer_does_not_create_retailer(self):
        invalid_data = {
            'firm_name': '',  # Missing required field
            'person_name': '',  # Missing required field
            'phone_number': '1234567890',
            'email_id': 'retailer@example.com',
            'address': '456 Retail Street'
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        print("Form Errors:", form.errors)
        retailer_exists = Retailer.objects.filter(
            email_id='retailer@example.com', user=self.user).exists()
        self.assertFalse(retailer_exists)

    def test_unique_firm_name_per_user(self):
        #Create a retailer with a specific firm name.
        Retailer.objects.create(
            user=self.user,
            firm_name='Test Retailer',
            person_name='Retailer Person',
            phone_number='1234567890',
            email_id='retailer@example.com',
            address='456 Retail Street'
        )
        #Attempt to create another retailer with the same firm name.
        with self.assertRaises(IntegrityError):
            Retailer.objects.create(
                user=self.user,
                firm_name='Test Retailer',
                person_name='Retailer Person',
                phone_number='1234567890',
                email_id='retailer2@example.com',
                address='789 Another Street'
            )

class ViewRetailersTest(TestCase):
    def setUp(self):
        """Set up a test user and sample retailers."""
        self.user = get_user_model().objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.retailer1 = Retailer.objects.create(
            user=self.user, firm_name="Test Retailer 1",
            person_name="Retailer Person 1", phone_number="1111111111",
            email_id="retailer1@example.com", address="111 Test Street"
        )
        self.retailer2 = Retailer.objects.create(
            user=self.user, firm_name="Test Retailer 2",
            person_name="Retailer Person 2", phone_number="2222222222",
            email_id="retailer2@example.com", address="222 Sample Road"
        )

    def test_view_retailers_list(self):
        response = self.client.get(reverse('view_retailers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'outward_supply/view_retailers.html')
        self.assertContains(response, "Test Retailer 1")
        self.assertContains(response, "Test Retailer 2")

    def test_search_retailers_by_firm_name(self):
        response = self.client.get(reverse('view_retailers'), {'query': 'Test Retailer 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Retailer 1")
        self.assertNotContains(response, "Test Retailer 2")

    def test_search_retailers_by_person_name(self):
        response = self.client.get(reverse('view_retailers'), {'query': 'Retailer Person 2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Retailer 2")
        self.assertNotContains(response, "Test Retailer 1")

    def test_edit_retailer(self):
        edit_url = reverse('edit_retailer', args=[self.retailer1.id])
        updated_data = {
            'firm_name': 'Updated Retailer',
            'person_name': 'Updated Person',
            'phone_number': '8888888888',
            'email_id': 'updatedretailer@example.com',
            'address': '888 Updated Street'
        }
        response = self.client.post(edit_url, updated_data)
        self.assertEqual(response.status_code, 302)                                # Redirects to view_retailers
        self.retailer1.refresh_from_db()
        self.assertEqual(self.retailer1.firm_name, 'Updated Retailer')
        self.assertEqual(self.retailer1.person_name, 'Updated Person')
        self.assertEqual(self.retailer1.phone_number, '8888888888')
        self.assertEqual(self.retailer1.email_id, 'updatedretailer@example.com')
        self.assertEqual(self.retailer1.address, '888 Updated Street')

    def test_delete_retailer(self):
        """Test deleting a retailer."""
        delete_url = reverse('delete_retailer', args=[self.retailer1.id])
        response = self.client.post(delete_url)                                      # Using POST for safety
        self.assertEqual(response.status_code, 302)                                  # Redirect to view_retailers
        self.assertFalse(Retailer.objects.filter(id=self.retailer1.id).exists())

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import json

from outward_supply.models import Outward_Invoice, ProductEntry, Retailer
from inventory.models import Inventory

class AddOutInvoiceTest(TestCase):
    def setUp(self):
        """Set up a test user, retailer, and two inventory products."""
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.retailer = Retailer.objects.create(
            user=self.user, firm_name="Test Retailer",
            person_name="Retailer Person", phone_number="1234567890",
            email_id="retailer@example.com",
            address="456 Retailer Street"
        )
        self.inventory_product1 = Inventory.objects.create(
            user=self.user, item_id="P001",
            product_name="Test Product 1", quantity=10,
            cost_price=Decimal('150.00'), sale_price=Decimal('200.00'),
            max_retail_price=Decimal('250.00'),
            gst=Decimal('10.00'),
        )
        self.inventory_product2 = Inventory.objects.create(
            user=self.user, item_id="P002",
            product_name="Test Product 2", quantity=20,
            cost_price=Decimal('250.00'), sale_price=Decimal('300.00'),
            max_retail_price=Decimal('350.00'),
            gst=Decimal('5.00'),
        )

    def test_get_add_out_invoice_page(self):
        url = reverse('add-outward-bill')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "outward_supply/add_outward_invoice.html")

    def test_post_valid_out_invoice_creates_invoice_and_product_entries(self):
        url = reverse('add-outward-bill')
        data = {
            'bill_number': 'INV100',
            'date': '2025-04-03',
            'billed-to': str(self.retailer.id),
            'discount': '10',
            'product_id[]': [str(self.inventory_product1.id), str(self.inventory_product2.id)],
            'quantity[]': ['5', '3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('out_invoice_list'))
        invoice = Outward_Invoice.objects.filter(user=self.user, bill_number='INV100').first()
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.retailer, self.retailer)
        product_entries = ProductEntry.objects.filter(invoice=invoice)
        self.assertEqual(product_entries.count(), 2)

        expected_amount1 = ((self.inventory_product1.sale_price * Decimal(5))*
                                            (1 + (self.inventory_product1.gst / Decimal(100))))
        expected_amount2 = ((self.inventory_product2.sale_price * Decimal(3))* 
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
        final_total = total_invoice_amount * (1 - Decimal(invoice.discount) / Decimal(100))
        self.assertEqual(Decimal(invoice.get_total_amount()), final_total)

    def test_post_duplicate_bill_number_shows_error(self):
        url = reverse('add-outward-bill')
        # Pre-create an invoice with a specific bill number
        Outward_Invoice.objects.create(user=self.user, bill_number='INV200', date='2025-04-03', discount=0)
        data = {
            'bill_number': 'INV100',
            'date': '2025-04-03',
            'discount': '0',
            'billed-to': str(self.retailer.id),
            'product_id[]': [str(self.inventory_product1.id)],
            'quantity[]': ['3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bill number already exists")

    def test_post_out_invoice_missing_required_field_shows_error(self):
        url = reverse('add-outward-bill')
        data = {
            # 'bill_number' is intentionally omitted
            'date': '2025-04-03',
            'discount': '5',
            'billed-to': str(self.retailer.id),
            'product_id[]': [str(self.inventory_product1.id), str(self.inventory_product2.id)],
            'quantity[]': ['5', '3']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required", msg_prefix="Missing bill number should trigger an error")
        self.assertEqual(Outward_Invoice.objects.count(), 0, "Invoice should not be created if required fields are missing.")

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from outward_supply.models import Retailer, Outward_Invoice, ProductEntry

class OutwardInvoiceListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        self.retailer = Retailer.objects.create( 
            user=self.user, firm_name='Test Firm',
            person_name='John Doe', phone_number='9876543210',
            email_id='john@example.com', address='123 Market Street',
        )
        self.invoice1 = Outward_Invoice.objects.create(
            user=self.user, date='2025-04-03',
            bill_number='INV001', retailer=self.retailer,
            discount=10.0,
            profit=5.0,
        )
        self.invoice2 = Outward_Invoice.objects.create(
            user=self.user, date='2025-04-03',
            bill_number='INV002', retailer=self.retailer,
            discount=5.0,
            profit=3.0,
        )
        ProductEntry.objects.create(invoice=self.invoice1, product_name='PRODUCT A', quantity=10, amount=50.0)
        ProductEntry.objects.create(invoice=self.invoice1, product_name='PRODUCT B', quantity=5, amount=25.0)
        ProductEntry.objects.create(invoice=self.invoice2, product_name='PRODUCT C', quantity=8, amount=32.0)

    def test_invoice_list_shows_all_user_invoices_with_details(self):
        response = self.client.get(reverse('out_invoice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "outward_supply/outward_invoice_list.html")

        self.assertContains(response, 'INV001')
        self.assertContains(response, 'INV002')
        self.assertContains(response, self.retailer.firm_name)

    def test_out_invoice_detail_shows_correct_invoice_and_products(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('out_invoice_detail', args=[self.invoice1.bill_number])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'outward_supply/out_invoice_detail.html')
        self.assertContains(response, self.invoice1.bill_number)
        self.assertNotContains(response, self.invoice2.bill_number)
        self.assertContains(response, 'PRODUCT A')
        self.assertContains(response, 'PRODUCT B')
        self.assertNotContains(response, 'PRODUCT C')
        self.assertContains(response, self.retailer.firm_name)

