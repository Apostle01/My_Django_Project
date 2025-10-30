# assign_images.py
import os
import re
from django.conf import settings
from products.models import Product

# Folder inside MEDIA_ROOT where your images live
IMAGE_SUBFOLDER = os.path.join("photos", "products")   # relative
IMAGE_FOLDER = os.path.join(settings.MEDIA_ROOT, IMAGE_SUBFOLDER)

# Normalize product name to a filename base, e.g. "Original Kente" -> "original-kente"
def normalize_name(name):
    # strip, lower, replace whitespace with dash, remove characters that break filenames
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)        # remove punctuation except underscore/dash/space
    s = re.sub(r"[\s_]+", "-", s)         # spaces/underscores -> dash
    return s

# Extensions to try (case-insensitive)
EXTS = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

assigned = 0
already = 0
not_found = 0
failed = 0

print("MEDIA_ROOT:", settings.MEDIA_ROOT)
print("Looking for images in:", IMAGE_FOLDER)
print("Products to inspect:", Product.objects.count())
print("-" * 60)

for product in Product.objects.all():
    try:
        name = product.name or ""
        norm = normalize_name(name)

        # If product already has an image name set, verify the file exists:
        if product.image and getattr(product.image, "name", ""):
            rel = product.image.name
            full = os.path.join(settings.MEDIA_ROOT, rel)
            if os.path.exists(full):
                print(f"[OK] {product.name} already has image: {rel}")
                already += 1
                continue
            else:
                print(f"[WARN] {product.name} had image field set to '{rel}' but file not found at '{full}'. Will attempt to reassign.")

        # Try candidate filenames
        found = False
        for ext in EXTS:
            candidate_filename = f"{norm}{ext}"
            candidate_full = os.path.join(IMAGE_FOLDER, candidate_filename)
            if os.path.exists(candidate_full):
                # relative path used for ImageField should use forward slashes
                rel_path = os.path.join(IMAGE_SUBFOLDER, candidate_filename).replace("\\", "/")
                product.image.name = rel_path
                product.save(update_fields=["image"])
                print(f"[ASSIGNED] {product.name} -> {rel_path}")
                assigned += 1
                found = True
                break

        if not found:
            print(f"[NO FILE] No matching image for product: '{product.name}' (tried base '{norm}')")
            not_found += 1

    except Exception as e:
        print(f"[ERROR] {product.name}: {e}")
        failed += 1

print("-" * 60)
print(f"Done. assigned={assigned}, already={already}, not_found={not_found}, failed={failed}")
