import os
import sys
import django
import csv
from django.utils.dateparse import parse_datetime
from django.contrib.auth.hashers import make_password
from django.db import connection

# Set up Django environment variables and paths
BASE_DIR = os.path.abspath(os.path.join(__file__, *[os.pardir] * 3))
sys.path.append(BASE_DIR)

# Ensure the DJANGO_SETTINGS_MODULE environment variable is set
os.environ['DJANGO_SETTINGS_MODULE'] = 'inventory_uts.settings'

# Initialize Django setup
django.setup()

# Now that Django is set up, we can import Django-specific modules
from django.contrib.auth.models import User
from core.models import Admin, Category, Supplier, Item

# Set directory where CSV files are stored
filepath = './data/'  # Adjust the path as needed

# Function to reset table ID sequence without TRUNCATE
def reset_table_sequence(model, sequence_name):
    model.objects.all().delete()  # Clear all data in the table
    with connection.cursor() as cursor:
        cursor.execute(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;")  # Reset sequence to 1

# Additional function to reset auth_user table
def reset_auth_user_sequence():
    User.objects.all().delete()  # Clear all data in auth_user table
    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;")  # Reset sequence to 1
    print("auth_user table reset successfully.")

# Import Admin data
def import_admins():
    reset_table_sequence(Admin, 'core_admin_id_seq')  # Reset ID sequence for Admin
    with open(filepath + 'admins.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if not Admin.objects.filter(username=row['username']).exists():
                # Create corresponding user in Django's auth_user table with is_superuser and is_staff set to True
                user = User.objects.create_user(
                    username=row['username'],
                    password=row['password'],
                    email=row['email']
                )
                user.is_superuser = True
                user.is_staff = True
                user.save()
                
                # Create Admin object
                obj_create.append(Admin(
                    username=row['username'],
                    password=make_password(row['password']),
                    email=row['email'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
                
        Admin.objects.bulk_create(obj_create)
    print("Admin data imported successfully.")

# Import Category data
def import_categories():
    reset_table_sequence(Category, 'core_category_id_seq')  # Reset ID sequence for Category
    with open(filepath + 'categories.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Admin.objects.filter(id=row['created_by_id']).exists():
                obj_create.append(Category(
                    name=row['name'],
                    description=row['description'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Admin with ID {row['created_by_id']} not found, skipping category {row['name']}.")
        Category.objects.bulk_create(obj_create)
    print("Category data imported successfully.")

# Import Supplier data
def import_suppliers():
    reset_table_sequence(Supplier, 'core_supplier_id_seq')  # Reset ID sequence for Supplier
    with open(filepath + 'suppliers.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Admin.objects.filter(id=row['created_by_id']).exists():
                obj_create.append(Supplier(
                    name=row['name'],
                    contact_info=row['contact_info'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Admin with ID {row['created_by_id']} not found, skipping supplier {row['name']}.")
        Supplier.objects.bulk_create(obj_create)
    print("Supplier data imported successfully.")

# Import Item data
def import_items():
    reset_table_sequence(Item, 'core_item_id_seq')  # Reset ID sequence for Item
    with open(filepath + 'items.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        obj_create = []
        for row in reader:
            if Category.objects.filter(id=row['category_id']).exists() and Supplier.objects.filter(id=row['supplier_id']).exists():
                obj_create.append(Item(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    quantity=row['quantity'],
                    category_id=row['category_id'],
                    supplier_id=row['supplier_id'],
                    created_by_id=row['created_by_id'],
                    created_at=parse_datetime(row['created_at']),
                    updated_at=parse_datetime(row['updated_at'])
                ))
            else:
                print(f"Category or supplier not found for item {row['name']}, skipping item.")
        Item.objects.bulk_create(obj_create)
    print("Item data imported successfully.")

# Run the import functions
if __name__ == "__main__":
    reset_auth_user_sequence()  # Reset auth_user table
    import_admins()
    import_categories()
    import_suppliers()
    import_items()
    print("Data import process completed.")
