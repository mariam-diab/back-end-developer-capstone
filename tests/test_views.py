from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create test data
        self.pizza = Menu.objects.create(Title='Pizza', Price=12.99, Inventory=10)
        self.burger = Menu.objects.create(Title='Burger', Price=8.99, Inventory=5)
        self.pasta = Menu.objects.create(Title='Pasta', Price=15.99, Inventory=7)

    def loginAsTestUser(self):
        self.client.login(username='testuser', password='testpassword')
    
    def test_view_authentication(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.loginAsTestUser()
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getall(self):
        self.loginAsTestUser()
        
        # Ensure test data is created
        menu = Menu.objects.all()
        print("Menu count:", menu.count())
        for item in menu:
            print(item)

        response = self.client.get(reverse('menu-items'))
        print("Response data:", response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = MenuSerializer(menu, many=True)
        print("Serialized data:", serializer.data)
        self.assertEqual(response.json(), serializer.data)
