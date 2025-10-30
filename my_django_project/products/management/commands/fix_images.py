import os
import re
import random
from django.core.management.base import BaseCommand
from products.models import Product, Category
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Fix product images: update, delete missing, auto-create from media/photos/products/, and assign categories"

    def handle(self, *args, **options):
        base_path = os.path.join("media", "photos", "products")
        extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]

        updated = 0
        deleted = 0
        created = 0

        # Step 1: Ensure categories exist
        categories_map = {
            "kente": "Kente Cloth",
            "gtp": "GTP Print",
            "akosombo": "Akosombo Textile",
            "woodin": "Woodin",
            "cloth": "Ghanaian Authentic Cloth",
        }

        for key, display_name in categories_map.items():
            Category.objects.get_or_create(name=display_name)

        # Step 2: Update or Delete existing products
        for product in Product.objects.all():
            base_filename = product.name.lower().replace(" ", "-")
            found_file = None

            for ext in extensions:
                candidate = os.path.join(base_path, base_filename + ext)
                if os.path.exists(candidate):
                    found_file = candidate
                    break

            if found_file:
                rel_path = os.path.relpath(found_file, "media")
                product.image = rel_path

                # Assign category if missing
                if not product.category:
                    assigned_category = self.get_category_from_name(product.name, categories_map)
                    if assigned_category:
                        product.category = assigned_category

                product.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"✔ Updated {product.name} → {rel_path}"))
            else:
                product.delete()
                deleted += 1
                self.stdout.write(self.style.WARNING(f"✘ Deleted {product.name} (no image found)"))

        # Step 3: Auto-create products for leftover image files
        existing_names = set(Product.objects.values_list("name", flat=True))
        for filename in os.listdir(base_path):
            name, ext = os.path.splitext(filename)
            if ext not in extensions:
                continue

            # Convert filename → Product name
            display_name = re.sub(r"[-_]+", " ", name).title()

            if display_name not in existing_names:
                rel_path = os.path.relpath(os.path.join(base_path, filename), "media")

                # Generate random price between 80 and 500 cedis
                price = round(random.uniform(80, 500), 2)

                # Generate a fake but nice description
                description = fake.sentence(nb_words=12)

                # Auto-assign category
                category = self.get_category_from_name(display_name, categories_map)

                new_product = Product.objects.create(
                    name=display_name,
                    description=description,
                    price=price,
                    image=rel_path,
                    category=category,
                )
                created += 1
                existing_names.add(display_name)
                self.stdout.write(
                    self.style.SUCCESS(f"➕ Created {new_product.name} (₵{price}, {category}) → {rel_path}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Done. Updated {updated}, Deleted {deleted}, Created {created} products.")
        )

    def get_category_from_name(self, name, categories_map):
        """Match product name to category based on keywords"""
        name_lower = name.lower()
        for key, display_name in categories_map.items():
            if key in name_lower:
                return Category.objects.get(name=display_name)
        return None
