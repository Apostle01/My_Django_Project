# my_django_project

A modern Django-based web application designed with clean architecture, reusable components, and a fully functional shopping workflow. The project includes product browsing, category filtering, a shopping bag system, and a checkout workflow with integrated payment support.

---

## 🚀 Features

- Dynamic homepage with featured content  
- Product catalog with category filtering  
- Detailed product pages  
- Add-to-bag and item quantity management  
- Shopping bag summary page  
- Secure checkout workflow  
- User authentication (registration, login, logout)  
- Responsive Bootstrap 4 front-end  
- Django admin panel with image support  

### 🎨 Category Filtering
- Dynamic category dropdown in the navbar  
- SEO-friendly URLs using slugs  
- Dedicated category pages showing filtered products  

### 🔎 Search
- Search products by name or description  
- Integrated search bar in the Shop page  

### 👤 User Accounts
- Registration, login, and logout using Django Allauth  
- Support for user-specific actions (reviews, order history, etc.)  

### 📝 Reviews
- Authenticated users can submit one review per product  
- Reviews displayed on product detail pages  

### 🗂️ Admin Control
- Manage products, categories, and images in Django Admin  
- Add, edit, and delete products securely  
- Image handling through Django media system  

---

## 🛠️ Tech Stack

- **Python 3.14**
- **Django 5**
- **SQLite** (development)
- **Bootstrap 4** for responsive UI
- **Stripe** (or your chosen gateway) for payments
- **Pillow** for image handling

---

## 📂 Project Structure

```plaintext
my_django_project/
│
├── home/
├── products/
├── bag/
├── payment/
├── templates/
├── static/
└── ...

## 🔧 Installation & Setup
### 1. Clone the repository
git clone <your-repo-url>
cd my_django_project

2. Create and activate a virtual environment
python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py migrate

5. Create a superuser (optional)
python manage.py createsuperuser

6. Run the development server
python manage.py runserver

📷 Media & Static Files

Uploaded product images are stored in the media/ directory.

Static files (CSS, JS, images) are located under static/.

💳 Payments

The project supports online payments.
Update your payment keys in:

payment/views.py
payment/settings.py


(Depending on your implementation.)

🧩 Customization

You can customize:

Templates (templates/)

Product categories

Payment logic

Navigation layout

Styling (Bootstrap 4)

📝 License

This project is provided for educational and development purposes.
You may extend or modify it freely.

👤 Author

Developed by Apostle.


---
