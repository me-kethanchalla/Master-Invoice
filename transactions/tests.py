from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from inward_supply.models import Supplier
from outward_supply.models import Retailer
from transactions.models import Transaction

class TransactionSupplierTest(TestCase):
    def setUp(self):
        """Set up a test user and sample suppliers."""
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.supplier1 = Supplier.objects.create(
            user=self.user, 
            firm_name="Supplier 1",
            person_name="Person 1", 
            phone_number="1111111111",
            email_id="supplier1@example.com", 
            address="111 Test Street",
            debit=500.0, 
            total_sales=1000.0
        )
        self.supplier2 = Supplier.objects.create(
            user=self.user, 
            firm_name="Supplier 2",
            person_name="Person 2", 
            phone_number="2222222222",
            email_id="supplier2@example.com", 
            address="222 Sample Road",
            debit=800.0, 
            total_sales=2000.0
        )

    def test_view_add_transaction_page(self):
        response = self.client.get(reverse('update_transaction_supplier'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/add_inward_transaction.html')

    def test_update_transaction_supplier(self):
        update_url = reverse('update_transaction_supplier')
        data = {
            'firm_name[]': ['Supplier 1', 'Supplier 2'],
            'amount_paid[]': ['100', '200'],
            'remarks[]': ['Paid in cash', 'Bank transfer'],
            'add_date': '2025-04-03'
        }
        response = self.client.post(update_url, data)
        self.assertRedirects(response, reverse('view_transaction_history'))

        transactions = Transaction.objects.filter(user=self.user, add_date='2025-04-03')
        self.assertEqual(transactions.count(), 2)

        trans_supplier1 = transactions.filter(firm_name="Supplier 1").first()
        self.assertIsNotNone(trans_supplier1)
        self.assertEqual(trans_supplier1.payment, 100.0)
        self.assertEqual(trans_supplier1.remarks, 'Paid in cash')
        self.assertEqual(trans_supplier1.person_name, 'Person 1')

        trans_supplier2 = transactions.filter(firm_name="Supplier 2").first()
        self.assertIsNotNone(trans_supplier2)
        self.assertEqual(trans_supplier2.payment, 200.0)
        self.assertEqual(trans_supplier2.remarks, 'Bank transfer')
        self.assertEqual(trans_supplier2.person_name, 'Person 2')

class TransactionRetailerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.retailer1 = Retailer.objects.create(
            user=self.user,
            firm_name="Retailer 1",
            person_name="Retailer Person 1",
            phone_number="3333333333",
            email_id="retailer1@example.com",
            address="333 Retailer Street",
            credit=1000.0
        )
        self.retailer2 = Retailer.objects.create(
            user=self.user,
            firm_name="Retailer 2",
            person_name="Retailer Person 2",
            phone_number="4444444444",
            email_id="retailer2@example.com",
            address="444 Retailer Avenue",
            credit=1500.0
        )

    def test_view_update_transaction_retailer_page(self):
        response = self.client.get(reverse('update_transaction_retailer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/pending.html')

    def test_update_transaction_retailer(self):
        update_url = reverse('update_transaction_retailer')
        data = {
            'firm_name[]': ['Retailer 1', 'Retailer 2'],
            'amount_paid[]': ['150', '250'],
            'remarks[]': ['Payment A', 'Payment B'],
            'add_date': '2025-04-03'
        }
        response = self.client.post(update_url, data)
        self.assertRedirects(response, reverse('view_transaction_history'))

        transactions = Transaction.objects.filter(user=self.user, add_date='2025-04-03')
        self.assertEqual(transactions.count(), 2)

        trans_retailer1 = transactions.filter(firm_name="Retailer 1").first()
        self.assertIsNotNone(trans_retailer1)
        self.assertEqual(trans_retailer1.payment, 150.0)
        self.assertEqual(trans_retailer1.remarks, 'Payment A')
        self.assertEqual(trans_retailer1.person_name, 'Retailer Person 1')
        self.assertEqual(trans_retailer1.type, 1)

        trans_retailer2 = transactions.filter(firm_name="Retailer 2").first()
        self.assertIsNotNone(trans_retailer2)
        self.assertEqual(trans_retailer2.payment, 250.0)
        self.assertEqual(trans_retailer2.remarks, 'Payment B')
        self.assertEqual(trans_retailer2.person_name, 'Retailer Person 2')
        self.assertEqual(trans_retailer2.type, 1)

class ViewTransactionHistoryTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.supplier = Supplier.objects.create(
            user=self.user,
            firm_name="Test Supplier",person_name="Supplier Person",
            phone_number="1111111111",email_id="supplier@example.com",
            address="Supplier Address",debit=100.0,total_sales=500.0
        )
        self.retailer = Retailer.objects.create(
            user=self.user, firm_name="Test Retailer", person_name="Retailer Person",
            phone_number="2222222222",email_id="retailer@example.com",
            address="Retailer Address", credit=1000.0
        )
        self.supplier_transaction = Transaction.objects.create(
            user=self.user,firm_name="Test Supplier",
            person_name="Supplier Person",add_date="2025-04-03",
            payment=50.0,remarks="Supplier transaction",type=0  # Supplier transaction
        )
        self.retailer_transaction = Transaction.objects.create(
            user=self.user,firm_name="Test Retailer",
            person_name="Retailer Person",add_date="2025-04-03",
            payment=75.0,remarks="Retailer transaction",type=1  # Retailer transaction
        )

    def test_view_transaction_history(self):
        url = reverse('view_transaction_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/view_transaction_history.html')

        self.assertIn(self.supplier, response.context['suppliers'])
        self.assertIn(self.retailer, response.context['retailers'])
        transactions = response.context['transactions']

        self.assertEqual(transactions.count(), 2)
        self.assertIn(self.supplier_transaction, transactions)
        self.assertIn(self.retailer_transaction, transactions)

        supplier_trans = transactions.filter(firm_name="Test Supplier").first()
        retailer_trans = transactions.filter(firm_name="Test Retailer").first()
        self.assertIsNotNone(supplier_trans)
        self.assertIsNotNone(retailer_trans)
        self.assertEqual(supplier_trans.payment, 50.0)
        self.assertEqual(supplier_trans.remarks, "Supplier transaction")
        self.assertEqual(retailer_trans.payment, 75.0)
        self.assertEqual(retailer_trans.remarks, "Retailer transaction")

class PendingViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.supplier1 = Supplier.objects.create(
            user=self.user, 
            firm_name="Supplier 1",
            person_name="Person 1", 
            phone_number="1111111111",
            email_id="supplier1@example.com", 
            address="111 Test Street",
            debit=500.0, 
            total_sales=1000.0
        )
        self.retailer1 = Retailer.objects.create(
            user=self.user, 
            firm_name="Retailer 1",
            person_name="Retailer Person 1", 
            phone_number="2222222222",
            email_id="retailer1@example.com", 
            address="222 Sample Road",
            credit=300.0, 
            total_sales=1500.0
        )

    def test_pending_view(self):
        response = self.client.get(reverse('pending'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/pending.html')

        response = self.client.get(reverse('pending'))
        self.assertIn(self.supplier1, response.context['suppliers'])
        self.assertIn(self.retailer1, response.context['retailers'])
