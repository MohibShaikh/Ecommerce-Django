from django.core.management.base import BaseCommand
from shop.models import Product
from datetime import date

class Command(BaseCommand):
    help = 'Adds sample products to the database'

    def handle(self, *args, **kwargs):
        products = [
            {
                'product_name': 'Premium Wireless Headphones',
                'category': 'Electronics',
                'subcategory': 'Audio',
                'price': 199,
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
                'pub_date': date.today(),
                'image': 'shop/images/headphones.jpg'
            },
            {
                'product_name': 'Smart Fitness Watch',
                'category': 'Electronics',
                'subcategory': 'Wearables',
                'price': 149,
                'description': 'Track your fitness goals with this advanced smartwatch featuring heart rate monitoring and GPS.',
                'pub_date': date.today(),
                'image': 'shop/images/smartwatch.jpg'
            },
            {
                'product_name': 'Professional Blender',
                'category': 'Home',
                'subcategory': 'Kitchen',
                'price': 89,
                'description': 'Powerful blender perfect for smoothies, soups, and more. 1000W motor with 6-speed settings.',
                'pub_date': date.today(),
                'image': 'shop/images/blender.jpg'
            },
            {
                'product_name': 'Ergonomic Office Chair',
                'category': 'Furniture',
                'subcategory': 'Office',
                'price': 249,
                'description': 'Comfortable office chair with adjustable height, lumbar support, and breathable mesh back.',
                'pub_date': date.today(),
                'image': 'shop/images/chair.jpg'
            },
            {
                'product_name': 'Portable Power Bank',
                'category': 'Electronics',
                'subcategory': 'Accessories',
                'price': 49,
                'description': '20000mAh power bank with fast charging and multiple USB ports for all your devices.',
                'pub_date': date.today(),
                'image': 'shop/images/powerbank.jpg'
            },
            {
                'product_name': 'Wireless Gaming Mouse',
                'category': 'Electronics',
                'subcategory': 'Gaming',
                'price': 79,
                'description': 'High-precision gaming mouse with customizable RGB lighting and programmable buttons.',
                'pub_date': date.today(),
                'image': 'shop/images/mouse.jpg'
            },
            {
                'product_name': 'Smart LED TV 55"',
                'category': 'Electronics',
                'subcategory': 'TV',
                'price': 699,
                'description': '4K Ultra HD Smart TV with HDR, built-in streaming apps, and voice control.',
                'pub_date': date.today(),
                'image': 'shop/images/tv.jpg'
            },
            {
                'product_name': 'Wireless Earbuds',
                'category': 'Electronics',
                'subcategory': 'Audio',
                'price': 129,
                'description': 'True wireless earbuds with active noise cancellation and 24-hour battery life.',
                'pub_date': date.today(),
                'image': 'shop/images/earbuds.jpg'
            }
        ]

        for product_data in products:
            Product.objects.create(**product_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully added product "{product_data["product_name"]}"')) 