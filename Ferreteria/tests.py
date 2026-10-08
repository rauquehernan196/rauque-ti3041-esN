from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class DashboardAndProductsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='password123',
            is_staff=True,
            is_superuser=True,
        )
        self.active_product = Producto.objects.create(
            nombre='Taladro Percutor',
            categoria='Herramientas Eléctricas',
            precio=39990,
            stock=8,
            archivado=False,
        )
        self.archived_product = Producto.objects.create(
            nombre='Sierra Manual',
            categoria='Herramientas Manuales',
            precio=8990,
            stock=12,
            archivado=True,
        )

    def test_feed_excludes_archived_products(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.active_product.nombre)
        self.assertNotContains(response, self.archived_product.nombre)

    def test_admin_dashboard_requires_staff_login(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_customers_can_register_and_add_items_to_cart(self):
        response = self.client.post(
            reverse('registro'),
            {
                'username': 'cliente',
                'email': 'cliente@correo.com',
                'password1': 'Clave123!',
                'password2': 'Clave123!',
            },
        )
        self.assertEqual(response.status_code, 302)

        self.client.login(username='cliente', password='Clave123!')
        response = self.client.post(reverse('agregar_al_carrito', args=[self.active_product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.active_product.pk), self.client.session.get('carrito', {}))

    def test_confirmar_compra_requires_login(self):
        response = self.client.post(reverse('confirmar_compra'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/cuenta/login/', response.url)
