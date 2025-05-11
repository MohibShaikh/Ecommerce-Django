# BuyEverything - Django Ecommerce Platform

BuyEverything is a modern, professional ecommerce web application built with Django. It features a product catalog, shopping cart, blog, order tracking, and a beautiful responsive design.

## Features
- Product catalog with categories
- Add to cart (with live cart count and modal pop-up)
- Edit/remove items in cart
- Checkout and order placement
- Order tracking
- Blog section
- Contact form
- Responsive, modern UI with Bootstrap 4, Font Awesome, and Google Fonts
- Pakistani Rupees (₨) currency support

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MohibShaikh/Ecommerce-Django.git
   cd Ecommerce-Django
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (optional, for admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Add sample products and images:**
   ```bash
   python manage.py add_sample_products
   python manage.py download_product_images
   ```
7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
8. **Visit the site:**
   Open [http://127.0.0.1:8000/shop/](http://127.0.0.1:8000/shop/) in your browser.

## Usage
- Browse products and add them to your cart.
- Click the cart button in the navbar to view/edit your cart in a pop-up modal.
- Proceed to checkout to place your order.
- Track your order using the tracker page.
- Read the latest posts in the blog section.

## Project Structure
- `shop/` - Main ecommerce app (products, cart, checkout, etc.)
- `blog/` - Blog app
- `media/` - Uploaded product images
- `templates/` - HTML templates

## Credits
- Product images from [Unsplash](https://unsplash.com/)
- UI: Bootstrap 4, Font Awesome, Google Fonts

---
For any issues or contributions, please open an issue or pull request.
 
