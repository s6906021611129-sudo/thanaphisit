"""config.py - ค่าคงที่ของโปรแกรม (ที่อยู่ไฟล์ และโครงสร้างฟิลด์)"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PRODUCT_FILE = os.path.join(DATA_DIR, "products.csv")
SALES_FILE = os.path.join(DATA_DIR, "sales.csv")

# ไฟล์ข้อมูลสินค้า
PRODUCT_FIELDS = ["product_id", "product_name", "category", "price", "stock"]

# ไฟล์ข้อมูลการขาย
SALES_FIELDS = ["sale_id", "sale_date", "product_id", "quantity", "unit_price", "total"]
