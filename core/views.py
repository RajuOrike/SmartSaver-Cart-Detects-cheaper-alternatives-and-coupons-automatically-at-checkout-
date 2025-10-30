# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
#
# from .forms import RegisterForm
# from .models import Coupon
# from django.utils import timezone
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# # ------------------- AUTH VIEWS -------------------
#
# def home(request):
#     return render(request, 'core/home.html')
#
#
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful.')
#             return redirect('home')
#     else:
#         form = RegisterForm()
#     return render(request, 'core/register.html', {'form': form})
#
#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('home')
#         messages.error(request, 'Invalid credentials')
#     return render(request, 'core/login.html')
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('home')
#
# # ------------------- AMAZON SCRAPING -------------------
#
# def scrape_amazon(query):
#     """Scrape Amazon India for real products"""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
#     driver.get(url)
#     time.sleep(3)
#
#     products = []
#     items = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
#
#     # ✅ Increased limit to 30 (was 6)
#     for item in items[:30]:
#         try:
#             title = item.find_element(By.TAG_NAME, "h2").text
#             price_el = item.find_element(By.CSS_SELECTOR, "span.a-price-whole")
#             link_el = item.find_element(By.TAG_NAME, "a")
#             image_el = item.find_element(By.CSS_SELECTOR, "img.s-image")
#
#             price_text = price_el.text.replace(",", "").strip()
#             if price_text:
#                 price = float(price_text)
#                 products.append({
#                     "title": title,
#                     "price": price,
#                     "link": link_el.get_attribute("href"),
#                     "image": image_el.get_attribute("src"),
#                     "source": "Amazon"
#                 })
#         except Exception:
#             continue
#
#     driver.quit()
#     print(len(products), "Amazon results found")
#     return products
#
#
# # ------------------- PRODUCT SEARCH -------------------
#
# def search_product(request):
#     query = request.GET.get("q")
#     products = []
#     coupons = Coupon.objects.all()
#
#     if query:
#         amazon_results = scrape_amazon(query)
#         products = sorted(amazon_results, key=lambda x: x["price"])  # Sort by price low → high
#
#     return render(request, "core/search_results.html", {
#         "products": products,
#         "query": query,
#         "coupons": coupons
#     })
#
#
# # ------------------- DUMMY COUPON SYSTEM -------------------
#
# def fetch_live_coupons(store):
#     """Simulated coupon fetch for demonstration"""
#     dummy_coupons = [
#         {"code": "AMZ10", "discount_percent": 10, "min_amount": 500, "store": "Amazon"},
#         {"code": "AMZ15", "discount_percent": 15, "min_amount": 2000, "store": "Amazon"},
#         {"code": "SAVE100", "discount_percent": 5, "min_amount": 500, "store": "Amazon"},
#         {"code": "SUPER20", "discount_percent": 20, "min_amount": 3000, "store": "Amazon"},
#     ]
#     return [c for c in dummy_coupons if c["store"].lower() == store.lower()]
#
# # ------------------- APPLY COUPON TO SINGLE PRODUCT -------------------
#
# @csrf_exempt
# @login_required
# def apply_coupon_single(request):
#     """Apply a coupon to a single product checkout using dummy coupons"""
#     if request.method == "POST":
#         code = request.POST.get("code", "").strip()
#         store = request.POST.get("store", "").strip()
#         price = float(request.POST.get("price", "0"))
#         product_link = request.POST.get("product_link", "")
#
#         coupons = fetch_live_coupons(store)
#         matched = next((c for c in coupons if c["code"].lower() == code.lower()), None)
#
#         if matched:
#             if price >= matched["min_amount"]:
#                 discount = (matched["discount_percent"] / 100) * price
#                 new_total = price - discount
#                 return render(request, "core/coupon_result.html", {
#                     "success": True,
#                     "original": price,
#                     "new_total": round(new_total, 2),
#                     "saved": round(discount, 2),
#                     "coupon": matched,
#                     "store": store,
#                     "product_link": product_link,
#                 })
#             else:
#                 return render(request, "core/coupon_result.html", {
#                     "error": f"Coupon valid only for orders above ₹{matched['min_amount']}.",
#                 })
#         else:
#             return render(request, "core/coupon_result.html", {
#                 "error": "❌ Invalid coupon or not applicable for this store.",
#             })
#
#     return render(request, "core/coupon_result.html", {
#         "error": "Invalid request method.",
#     })
#
# # ------------------- CHECKOUT SIMULATION -------------------
#
# @login_required
# def checkout_simulate(request):
#     """Simulate checkout with best coupon selection"""
#     items = request.POST.getlist('item_price')
#     items = [float(x) for x in items] if items else []
#     store = request.POST.get('store', 'Amazon')
#     coupon_code = request.POST.get('coupon_code', '').strip()
#     total = sum(items)
#     applied = None
#     final_total = total
#
#     if coupon_code:
#         try:
#             coupon = Coupon.objects.get(code__iexact=coupon_code)
#             if coupon.is_valid(total, store):
#                 final_total = coupon.apply_discount(total)
#                 applied = coupon
#         except Coupon.DoesNotExist:
#             applied = None
#
#     best = None
#     best_total = final_total
#     for c in Coupon.objects.filter(active=True):
#         if c.is_valid(total, store):
#             t = c.apply_discount(total)
#             if t < best_total:
#                 best_total = t
#                 best = c
#
#     context = {
#         'items': items,
#         'store': store,
#         'total': total,
#         'applied_coupon': applied,
#         'final_total': round(final_total, 2),
#         'auto_best_coupon': best,
#         'auto_best_total': round(best_total, 2),
#     }
#     return render(request, 'core/checkout.html', context)
#
#
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
from .models import Coupon
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ------------------- AUTH VIEWS -------------------

def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# ------------------- AMAZON SCRAPING -------------------

def scrape_amazon(query):
    """Scrape Amazon India for real products"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(3)

    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")

    # ✅ Increased limit to 30 (was 6)
    for item in items[:30]:
        try:
            title = item.find_element(By.TAG_NAME, "h2").text
            price_el = item.find_element(By.CSS_SELECTOR, "span.a-price-whole")
            link_el = item.find_element(By.TAG_NAME, "a")
            image_el = item.find_element(By.CSS_SELECTOR, "img.s-image")

            price_text = price_el.text.replace(",", "").strip()
            if price_text:
                price = float(price_text)
                products.append({
                    "title": title,
                    "price": price,
                    "link": link_el.get_attribute("href"),
                    "image": image_el.get_attribute("src"),
                    "source": "Amazon"
                })
        except Exception:
            continue

    driver.quit()
    print(len(products), "Amazon results found")
    return products

# ------------------- MYNTRA SCRAPING -------------------

def scrape_myntra(query):
    """Scrape Myntra products using Selenium"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        url = f"https://www.myntra.com/{query.replace(' ', '%20')}"  # More specific URL for shoes
        print(f"Myntra: Accessing URL {url}")
        driver.get(url)

        # Scroll multiple times to load more products
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
        )

        products = []
        items = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        #print(f"Myntra: Found {len(items)} product items")

        for item in items[:30]:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h3.product-brand, div.product-brand").text
                name = item.find_element(By.CSS_SELECTOR, "h4.product-product, div.product-product").text
                # Filter for shoes-related products
                if not any(keyword in name.lower() for keyword in ['shoe', 'sneaker', 'sandal', 'boot', 'footwear']):
                    #print(f"Myntra item skipped (not a shoe): {title} - {name}")
                    continue
                price_el = item.find_element(By.CSS_SELECTOR, "span.product-discountedPrice, span.product-price, div.product-price")
                link_el = item.find_element(By.CSS_SELECTOR, "a")
                # Updated image selector to handle lazy-loaded images and common classes
                img_el = item.find_element(By.CSS_SELECTOR,
                    "img[src*='images'], img[class*='product'], img[class*='thumbnail'], img[data-src*='images'], picture img, img")
                price_text = price_el.text.replace("₹", "").replace(",", "").strip()
                # Extract only the discounted price (e.g., "Rs. 989Rs. 2199(55% OFF)" -> "989")
                price_match = re.match(r'Rs\.\s*(\d+)', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    image_url = img_el.get_attribute("data-src") or img_el.get_attribute("src")  # Handle lazy-loaded images
                    products.append({
                        "title": f"{title} - {name}",
                        "price": price,
                        "link": link_el.get_attribute("href"),
                        "image": image_url,
                        "source": "Myntra"
                    })
            except Exception as e:
               # print(f"Myntra item error: {str(e)}")
                continue

        # Save page source for debugging
        with open("myntra_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        driver.quit()
        print(len(products), "Myntra results found")
        return products

    except Exception as e:
       # print(f"Myntra scraping failed: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return []

# ------------------- PRODUCT SEARCH -------------------

def search_product(request):
    query = request.GET.get("q")
    products = []
    coupons = Coupon.objects.all()

    if query:
        amazon_results = scrape_amazon(query)
        products = sorted(amazon_results, key=lambda x: x["price"])  # Sort by price low → high

    if query:
        try:
            myntra_results = scrape_myntra(query)
        except Exception as e:
            print(f"Myntra scraping failed: {str(e)}")
            myntra_results = []

        # Merge all store results
        products = amazon_results + myntra_results
        products = sorted(products, key=lambda x: x["price"])  # Sort by lowest price

    return render(request, "core/search_results.html", {
        "products": products,
        "query": query,
        "coupons": coupons
    })

# ------------------- DUMMY COUPON SYSTEM -------------------

def fetch_live_coupons(store):
    """Simulated coupon fetch for demonstration"""
    dummy_coupons = [
        {"code": "AMZ10", "discount_percent": 10, "min_amount": 500, "store": "Amazon"},
        {"code": "AMZ15", "discount_percent": 15, "min_amount": 2000, "store": "Amazon"},
        {"code": "SAVE100", "discount_percent": 5, "min_amount": 500, "store": "Amazon"},
        {"code": "SUPER20", "discount_percent": 20, "min_amount": 3000, "store": "Amazon"},
        {"code": "MYN25", "discount_percent": 25, "min_amount": 1000, "store": "Myntra"},
    ]
    return [c for c in dummy_coupons if c["store"].lower() == store.lower()]

# ------------------- AUTO APPLY BEST COUPON -------------------

@csrf_exempt
@login_required
def apply_coupon_single(request):
    """Automatically apply the best coupon for a product based on conditions"""
    if request.method == "POST":
        store = request.POST.get("store", "").strip()
        price = float(request.POST.get("price", "0"))
        product_link = request.POST.get("product_link", "")

        coupons = fetch_live_coupons(store)
        valid_coupons = []

        for c in coupons:
            if price >= c["min_amount"]:
                discount_amount = (c["discount_percent"] / 100) * price
                final_price = price - discount_amount
                valid_coupons.append({
                    "coupon": c,
                    "discount": round(discount_amount, 2),
                    "final_price": round(final_price, 2)
                })

        if not valid_coupons:
            return render(request, "core/coupon_result.html", {
                "error": f"No valid coupons available for this price (₹{price}) on {store}."
            })

        best_coupon = max(valid_coupons, key=lambda x: x["discount"])
        best = best_coupon["coupon"]

        return render(request, "core/coupon_result.html", {
            "success": True,
            "original": price,
            "new_total": best_coupon["final_price"],
            "saved": best_coupon["discount"],
            "coupon": best,
            "store": store,
            "product_link": product_link,
            "auto_applied": True,
        })

    return render(request, "core/coupon_result.html", {
        "error": "Invalid request method.",
    })

# ------------------- CHECKOUT SIMULATION -------------------

@login_required
def checkout_simulate(request):
    """Simulate checkout with best coupon selection"""
    items = request.POST.getlist('item_price')
    items = [float(x) for x in items] if items else []
    store = request.POST.get('store', 'Amazon')
    coupon_code = request.POST.get('coupon_code', '').strip()
    total = sum(items)
    applied = None
    final_total = total

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code)
            if coupon.is_valid(total, store):
                final_total = coupon.apply_discount(total)
                applied = coupon
        except Coupon.DoesNotExist:
            applied = None

    best = None
    best_total = total
    for c in Coupon.objects.filter(active=True):
        if c.is_valid(total, store):
            t = c.apply_discount(total)
            if t < best_total:
                best_total = t
                best = c

    context = {
        'items': items,
        'store': store,
        'total': total,
        'applied_coupon': applied,
        'final_total': round(final_total, 2),
        'auto_best_coupon': best,
        'auto_best_total': round(best_total, 2),
    }
    return render(request, 'core/checkout.html', context)