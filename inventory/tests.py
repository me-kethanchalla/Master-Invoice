from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import Inventory
from django.db import IntegrityError

class AddInventoryModelViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.url = reverse('add_inventory')

    def test_get_request_returns_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/add_inventory.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context.get('message', ''), '')

    def test_post_valid_inventory_creates_product_and_redirects(self):
        valid_data = {
            'item_id': '12345',
            'product_name': 'Test Product',
            'quantity': 10,
            'cost_price': 50,
            'sale_price': 100,
            'max_retail_price': 120,
            'gst': 18
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)
        inventory_exists = Inventory.objects.filter(
            item_id='12345', user=self.user
        ).exists()
        self.assertTrue(inventory_exists)

    def test_post_invalid_inventory_does_not_create_product(self):
        invalid_data = {
            'item_id': '',  # Missing required value
            'product_name': '',
            'quantity': '',
            'cost_price': 50,
            'sale_price': 100,
            'max_retail_price': 120,
            'gst': 18
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        print("Form Errors:", form.errors)
        inventory_exists = Inventory.objects.filter(
            item_id='12345', user=self.user
        ).exists()
        self.assertFalse(inventory_exists)

    def test_unique_item_id_per_user(self):
        # Create an inventory item with a specific item_id.
        Inventory.objects.create(
            user=self.user,
            item_id='12345',
            product_name='Test Product',
            quantity=10,
            cost_price=50,
            sale_price=100,
            max_retail_price=120,
            gst=18,
            total_qty_sold=0
        )
        # Attempt to create another inventory item with the same item_id.
        with self.assertRaises(IntegrityError):
            Inventory.objects.create(
                user=self.user,
                item_id='12345',
                product_name='Duplicate Product',
                quantity=5,
                cost_price=60,
                sale_price=120,
                max_retail_price=150,
                gst=18,
                total_qty_sold=0
            )

class InventoryViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.item1 = Inventory.objects.create(
            user=self.user,
            item_id="12345",
            product_name="Test Product 1",
            quantity=10,
            cost_price=50,
            sale_price=100,
            max_retail_price=120,
            gst=18,
            total_qty_sold=0
        )
        self.item2 = Inventory.objects.create(
            user=self.user,
            item_id="67890",
            product_name="Test Product 2",
            quantity=5,
            cost_price=30,
            sale_price=80,
            max_retail_price=100,
            gst=18,
            total_qty_sold=0
        )

    def test_inventory_list_view(self):
        response = self.client.get(reverse('inventory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/inventory.html')
        self.assertContains(response, "Test Product 1")
        self.assertContains(response, "Test Product 2")

    def test_inventory_search_by_product_name(self):
        response = self.client.get(reverse('inventory_list'), {'query': 'Test Product 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 1")
        self.assertNotContains(response, "Test Product 2")


    def test_inventory_search_by_item_id(self):
        response = self.client.get(reverse('inventory_list'), {'query': '67890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product 2") 
        self.assertNotContains(response, "Test Product 1")


    def test_edit_inventory(self):
        edit_url = reverse('edit_inventory', args=[self.item1.id])
        updated_data = {
            'item_id': '12345',
            'product_name': 'Updated Product',
            'quantity': 15,
            'cost_price': 55,
            'sale_price': 110,
            'max_retail_price': 130,
            'gst': 18
        }
        response = self.client.post(edit_url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.product_name, 'Updated Product')
        self.assertEqual(self.item1.quantity, 15)
        self.assertEqual(self.item1.sale_price, 110)

    def test_delete_inventory(self):
        delete_url = reverse('delete_inventory', args=[self.item1.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        item_exists = Inventory.objects.filter(id=self.item1.id).exists()
        self.assertFalse(item_exists)
