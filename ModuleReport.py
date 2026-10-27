# ModuleReport.py : รายงานสรุปยอดขาย (โจทย์ข้อ c และ d)
from ModuleProduct import print_message, print_table, get_name


def daily_summary(sales):
    """ข้อ c : สรุปยอดขายรายวัน"""
    data = {}                                  # {วันที่: [จำนวนรายการ, จำนวนชิ้น, ยอดเงิน]}
    try:
        for s in sales:
            date = s[1]
            qty = int(s[3])
            total = float(s[5])
            try:
                data[date][0] += 1
                data[date][1] += qty
                data[date][2] += total
            except KeyError:                   # วันที่นี้ยังไม่เคยมีใน dict
                data[date] = [1, qty, total]
    except IndexError:
        print_message('ข้อมูลในไฟล์ไม่ครบทุกช่อง')
    except ValueError:
        print_message('ข้อมูลตัวเลขในไฟล์ไม่ถูกต้อง')
    else:
        rows = []
        all_total = 0
        for date in sorted(data):
            d = data[date]
            all_total += d[2]
            rows.append([date, d[0], d[1], f'{d[2]:,.2f}'])
        print_table('รายงานสรุปยอดขายรายวัน',
                    ['วันที่', 'จำนวนรายการ', 'จำนวนชิ้น', 'ยอดขาย'],
                    rows, ['<', '>', '>', '>'],
                    f'ยอดขายรวมทั้งหมด {all_total:,.2f} บาท')


def summary_by_product(products, sales):
    """ข้อ d : สรุปยอดขายตามข้อมูลสินค้า"""
    data = {}                                  # {รหัสสินค้า: [จำนวนชิ้น, ยอดเงิน]}
    try:
        for s in sales:
            prod_id = s[2]
            qty = int(s[3])
            total = float(s[5])
            try:
                data[prod_id][0] += qty
                data[prod_id][1] += total
            except KeyError:
                data[prod_id] = [qty, total]
    except IndexError:
        print_message('ข้อมูลในไฟล์ไม่ครบทุกช่อง')
    except ValueError:
        print_message('ข้อมูลตัวเลขในไฟล์ไม่ถูกต้อง')
    else:
        rows = []
        all_total = 0
        for prod_id in sorted(data):
            d = data[prod_id]
            all_total += d[1]
            rows.append([prod_id, get_name(products, prod_id), d[0], f'{d[1]:,.2f}'])
        print_table('รายงานสรุปยอดขายตามสินค้า',
                    ['รหัส', 'ชื่อสินค้า', 'จำนวนที่ขาย', 'ยอดขาย'],
                    rows, ['<', '<', '>', '>'],
                    f'ยอดขายรวมทั้งหมด {all_total:,.2f} บาท')
