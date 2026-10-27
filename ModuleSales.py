# ModuleSales.py : จัดการข้อมูลการขาย (โจทย์ข้อ b)
from datetime import datetime
from ModuleProduct import (ENC, print_title, print_message, print_table,
                           read_data, write_data, get_name, report_product)

SALES_FILE = 'sales.csv'


def add_sale(sales_file, product_file):
    print_title('บันทึกการขาย', 44)
    products = read_data(product_file)
    
    # ถ้าในระบบยังไม่มีข้อมูลสินค้า ให้แจ้งเตือนแล้วยกเลิกการทำงาน
    if not products:
        print_message('ยังไม่มีข้อมูลสินค้าในระบบ')
        return

    # --- ส่วนที่เพิ่มใหม่: โชว์รายการสินค้าทั้งหมดก่อนเลือกรหัส ---
    print_title('รายการสินค้าที่มีในระบบ', 44)
    report_product(products)

    prod_id = input('รหัสสินค้า : ').strip()
    found = None
    for p in products:
        if p[0] == prod_id:
            found = p
    if found is None:
        print_message('ไม่พบสินค้านี้')
        return
    price = float(found[2])
    stock = int(found[3])
    print_table('ข้อมูลสินค้าที่เลือก',
                ['รหัส', 'ชื่อสินค้า', 'ราคา', 'คงเหลือ'],
                [[found[0], found[1], f'{price:,.2f}', stock]],
                ['<', '<', '>', '>'])
    try:
        qty = int(input('จำนวนที่ขาย : '))
        date = input('วันที่ขาย (YYYY-MM-DD) : ').strip()
        datetime.strptime(date, '%Y-%m-%d')      # ตรวจรูปแบบวันที่
    except ValueError:
        print_message('จำนวนหรือวันที่ไม่ถูกต้อง ไม่บันทึกข้อมูล')
    else:
        if qty <= 0 or qty > stock:
            print_message('จำนวนต้องมากกว่า 0 และไม่เกินสต็อกคงเหลือ')
        else:
            sale_id = f'S{len(read_data(sales_file)) + 1:04d}'
            total = qty * price
            with open(sales_file, 'a', encoding=ENC) as fout:
                fout.write(f'{sale_id},{date},{prod_id},{qty},{price},{total}\n')
            found[3] = str(stock - qty)           # ตัดสต็อก
            write_data(product_file, products)
            print_table('บันทึกการขายเรียบร้อย',
                        ['เลขที่', 'วันที่', 'ชื่อสินค้า', 'จำนวน', 'ราคา/หน่วย', 'รวม'],
                        [[sale_id, date, found[1], qty, f'{price:,.2f}', f'{total:,.2f}']],
                        ['<', '<', '<', '>', '>', '>'])
    finally:
        print_message('จบการบันทึกการขาย')


def report_sales(products, sales):
    n = 0
    all_total = 0
    rows = []
    try:
        for s in sales:
            n += 1
            total = float(s[5])
            all_total += total
            rows.append([s[0], s[1], get_name(products, s[2]), int(s[3]),
                         f'{float(s[4]):,.2f}', f'{total:,.2f}'])
    except IndexError:
        print_message('ข้อมูลในไฟล์ไม่ครบทุกช่อง')
    except ValueError:
        print_message('ข้อมูลตัวเลขในไฟล์ไม่ใช่ตัวเลข')
    else:
        print_table('รายงานข้อมูลการขาย',
                    ['เลขที่', 'วันที่', 'ชื่อสินค้า', 'จำนวน', 'ราคา/หน่วย', 'รวม'],
                    rows, ['<', '<', '<', '>', '>', '>'],
                    f'รวม {n} รายการ   ยอดขายรวม {all_total:,.2f} บาท')