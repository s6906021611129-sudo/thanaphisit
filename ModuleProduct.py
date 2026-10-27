# ModuleProduct.py : จัดการข้อมูลสินค้า (โจทย์ข้อ a) + ฟังก์ชันอ่าน/เขียนไฟล์ + ฟังก์ชันพิมพ์ตาราง
import unicodedata

ENC = 'utf-8-sig'            # ให้ Excel เปิดภาษาไทยได้ถูกต้อง
PRODUCT_FILE = 'products.csv'


# ---------- ส่วนพิมพ์ตาราง (ใช้ร่วมกันทุกหน้า) ----------
def show_len(text):
    """ความยาวที่ตามองเห็นจริง : สระบน/ล่าง และวรรณยุกต์ภาษาไทยไม่กินพื้นที่ จึงไม่นับ"""
    n = 0
    for ch in str(text):
        if unicodedata.category(ch) != 'Mn':
            n += 1
    return n


def fit(text, width, align):
    """เติมช่องว่างให้ข้อความกว้าง width   align: '<' ชิดซ้าย, '>' ชิดขวา, '^' กึ่งกลาง"""
    text = str(text)
    gap = width - show_len(text)
    if gap < 0:
        gap = 0
    if align == '>':
        return ' ' * gap + text
    if align == '^':
        left = gap // 2
        return ' ' * left + text + ' ' * (gap - left)
    return text + ' ' * gap


def make_row(cells, widths, aligns):
    """สร้างบรรทัดข้อมูล 1 แถว  เช่น  | P001 | น้ำดื่ม |"""
    parts = []
    for i in range(len(cells)):
        parts.append(fit(cells[i], widths[i], aligns[i]))
    return '| ' + ' | '.join(parts) + ' |'


def print_title(title, width):
    """กล่องหัวข้อ (ใช้เป็นหัวของทุกหน้า)"""
    print('=' * width)
    print('|' + fit(title, width - 2, '^') + '|')
    print('=' * width)


def print_message(text):
    """แสดงข้อความแจ้งผลการทำงานในกล่อง"""
    print_title(text, max(30, show_len(text) + 4))
    print()


def print_table(title, headers, rows, aligns, footer=''):
    """พิมพ์ตารางแบบกล่อง ความกว้างแต่ละคอลัมน์ปรับตามข้อมูลที่ยาวที่สุดอัตโนมัติ"""
    widths = []
    for i in range(len(headers)):
        w = show_len(headers[i])
        for r in rows:
            if show_len(r[i]) > w:
                w = show_len(r[i])
        widths.append(w)
    total = sum(widths) + 3 * len(widths) + 1
    if show_len(title) + 4 > total:              # ชื่อตารางยาวกว่าตาราง ให้ขยายคอลัมน์สุดท้าย
        widths[-1] += show_len(title) + 4 - total
        total = show_len(title) + 4
    print_title(title, total)
    print(make_row(headers, widths, ['^'] * len(headers)))
    print('-' * total)
    for r in rows:
        print(make_row(r, widths, aligns))
    print('=' * total)
    if footer != '':
        print(footer)
    print()


# ---------- ส่วนอ่าน/เขียนไฟล์ ----------
def read_data(filename):
    """อ่านไฟล์ CSV คืนค่าเป็น list ของ list เช่น [['P001','น้ำดื่ม','10.0','97'], ...]"""
    data = []
    try:
        with open(filename, encoding=ENC) as fin:
            for line in fin:
                line = line.rstrip('\n')
                if line != '':
                    data.append(line.split(','))
    except FileNotFoundError:
        pass                 # ยังไม่มีไฟล์ = ยังไม่มีข้อมูล
    return data


def write_data(filename, data):
    """เขียนข้อมูลทั้งหมดทับไฟล์เดิม"""
    with open(filename, 'w', encoding=ENC) as fout:
        for row in data:
            fout.write(','.join(row) + '\n')


def get_name(products, prod_id):
    """หาชื่อสินค้าจากรหัส"""
    for p in products:
        if p[0] == prod_id:
            return p[1]
    return '(ไม่พบสินค้า)'


# ---------- ข้อ a : จัดการข้อมูลสินค้า ----------
def add_product(filename):
    print_title('เพิ่มข้อมูลสินค้า', 44)
    products = read_data(filename)
    prod_id = input('รหัสสินค้า : ').strip()
    prod_name = input('ชื่อสินค้า : ').strip()
    if prod_id == '' or prod_name == '':
        print_message('ต้องกรอกรหัสและชื่อสินค้า')
        return
    for p in products:
        if p[0] == prod_id:
            print_message('รหัสสินค้านี้มีอยู่แล้ว')
            return
    try:
        price = float(input('ราคา : '))
        qty = int(input('จำนวนคงเหลือ : '))
    except ValueError:
        print_message('กรอกตัวเลขไม่ถูกต้อง ไม่บันทึกข้อมูล')
    else:
        if price < 0 or qty < 0:
            print_message('ราคาและจำนวนต้องไม่ติดลบ')
        else:
            with open(filename, 'a', encoding=ENC) as fout:
                fout.write(f'{prod_id},{prod_name},{price},{qty}\n')
            print_table('บันทึกข้อมูลสินค้าเรียบร้อย',
                        ['รหัส', 'ชื่อสินค้า', 'ราคา', 'จำนวน'],
                        [[prod_id, prod_name, f'{price:,.2f}', qty]],
                        ['<', '<', '>', '>'])
    finally:
        print_message('จบการเพิ่มสินค้า')


def report_product(products):
    n = 0
    rows = []
    try:
        for p in products:
            n += 1
            rows.append([n, p[0], p[1], f'{float(p[2]):,.2f}', int(p[3])])
    except IndexError:
        print_message('ข้อมูลในไฟล์ไม่ครบทุกช่อง')
    except ValueError:
        print_message('ข้อมูลราคาหรือจำนวนในไฟล์ไม่ใช่ตัวเลข')
    else:
        print_table('รายงานข้อมูลสินค้า',
                    ['ที่', 'รหัส', 'ชื่อสินค้า', 'ราคา', 'จำนวน'],
                    rows, ['>', '<', '<', '>', '>'],
                    f'รวม {n} รายการ')
