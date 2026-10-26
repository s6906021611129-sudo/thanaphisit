"""main.py - จุดเริ่มต้นโปรแกรม (เมนูหลัก)   รัน:  python main.py"""
from pos.core import storage, utils
from pos.modules import product, reports, sales


def main():
    storage.ensure_files()
    while True:
        utils.print_menu("ระบบขายสินค้า (Point of Sale)", [
            "1. จัดการข้อมูลสินค้า", "2. จัดการข้อมูลการขาย",
            "3. รายงานสรุปยอดขายรายวัน", "4. รายงานสรุปยอดขายตามสินค้า",
            "0. ออกจากโปรแกรม"])
        choice = input("เลือกเมนู: ").strip()
        if choice == "1":
            product.menu()
        elif choice == "2":
            sales.menu()
        elif choice == "3":
            reports.daily_summary()
            utils.pause()
        elif choice == "4":
            reports.summary_by_product()
            utils.pause()
        elif choice == "0":
            print("ขอบคุณที่ใช้งานโปรแกรม")
            break
        else:
            print("  ! เมนูไม่ถูกต้อง")


if __name__ == "__main__":
    main()
