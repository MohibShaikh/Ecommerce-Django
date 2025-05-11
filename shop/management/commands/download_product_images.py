from django.core.management.base import BaseCommand
import requests
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Downloads sample product images from Unsplash'

    def handle(self, *args, **kwargs):
        # Create the images directory if it doesn't exist
        image_dir = os.path.join(settings.MEDIA_ROOT, 'shop', 'images')
        os.makedirs(image_dir, exist_ok=True)

        # Image URLs from Unsplash (free to use)
        image_urls = {
            'headphones.jpg': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80',
            'smartwatch.jpg': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80',
            'blender.jpg': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500&q=80',
            'chair.jpg': 'https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=500&q=80',
            'powerbank.jpg': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80',
            'mouse.jpg': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&q=80',
            'tv.jpg': 'https://images.unsplash.com/photo-1593784991095-a205069470b6?w=500&q=80',
            'earbuds.jpg': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=500&q=80'
        }

        for filename, url in image_urls.items():
            try:
                # Download the image
                response = requests.get(url)
                response.raise_for_status()

                # Save the image
                file_path = os.path.join(image_dir, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully downloaded {filename}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to download {filename}: {str(e)}')) 