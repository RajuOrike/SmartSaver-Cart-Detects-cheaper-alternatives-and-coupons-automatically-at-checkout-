SmartSaver Cart - Advanced Starter (Django)
==========================================

What you get:
- Django project with 'core' app implementing:
  - User registration/login (Django auth)
  - Mock product search (replace mock_scrape_for_query with real scraping/API)
  - Coupon model with validation and application
  - Checkout simulation that auto-suggests best coupon

Quick start (run locally):
1. Create and activate a virtualenv with Python 3.10+.
2. Install requirements:
   pip install -r requirements.txt
3. From project root (where manage.py lives):
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
4. Open http://127.0.0.1:8000

Notes:
- For real e-commerce scraping, implement dedicated scrapers (use Selenium for JS-heavy sites).
- Keep SECRET_KEY secure and set DEBUG=False in production.
