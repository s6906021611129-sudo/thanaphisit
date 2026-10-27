# main.py : โปรแกรมระบบขายสินค้า (Point of Sale)   รัน:  python main.py
from ModuleProduct import (PRODUCT_FILE, print_message, print_table,
                           read_data, add_product, report_product)
from ModuleSales import SALES_FILE, add_sale, report_sales
from ModuleReport import daily_summary, summary_by_product


def show_menu():
    rows = [['1', 'เพิ่มข้อมูลสินค้า'],
            ['2', 'รายงานข้อมูลสินค้า'],
            ['3', 'บันทึกการขาย'],
            ['4', 'รายงานข้อมูลการขาย'],
            ['5', 'รายงานสรุปยอดขายรายวัน'],
            ['6', 'รายงานสรุปยอดขายตามสินค้า'],
            ['0', 'ออกจากโปรแกรม']]
    print_table('ระบบขายสินค้า (Point of Sale)', ['เมนู', 'รายการ'], rows, ['^', '<'])


def main():
    while True:
        show_menu()
        choice = input('เลือกเมนู : ').strip()
        if choice == '1':
            add_product(PRODUCT_FILE)
        elif choice == '2':
            report_product(read_data(PRODUCT_FILE))
        elif choice == '3':
            add_sale(SALES_FILE, PRODUCT_FILE)
        elif choice == '4':
            report_sales(read_data(PRODUCT_FILE), read_data(SALES_FILE))
        elif choice == '5':
            daily_summary(read_data(SALES_FILE))
        elif choice == '6':
            summary_by_product(read_data(PRODUCT_FILE), read_data(SALES_FILE))
        elif choice == '0':
            break
        else:
            print_message('ไม่มีเมนูนี้ กรุณาเลือกใหม่')
    print_message('Exit Program')


if __name__ == '__main__':
    main()
