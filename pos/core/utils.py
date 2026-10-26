"""utils.py - ฟังก์ชันช่วยเหลือ: รับข้อมูลจากผู้ใช้ และแสดงตาราง"""
import unicodedata
from datetime import datetime


# ---------- รับข้อมูล ----------
def input_str(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  ! กรุณากรอกข้อมูล")


def input_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"  ! ต้องมีค่าตั้งแต่ {minimum} ขึ้นไป")
        except ValueError:
            print("  ! กรุณากรอกจำนวนเต็ม")


def input_float(prompt, minimum=0.0):
    while True:
        try:
            value = float(input(prompt))
            if value >= minimum:
                return value
            print(f"  ! ต้องมีค่าตั้งแต่ {minimum} ขึ้นไป")
        except ValueError:
            print("  ! กรุณากรอกตัวเลข")


def input_date(prompt, default_today=True):
    """รับวันที่รูปแบบ YYYY-MM-DD (กด Enter = วันนี้)"""
    today = datetime.now().strftime("%Y-%m-%d")
    while True:
        text = input(prompt + (f" [Enter = {today}]: " if default_today else ": ")).strip()
        if not text and default_today:
            return today
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("  ! รูปแบบวันที่ต้องเป็น YYYY-MM-DD เช่น 2026-10-26")


def confirm(prompt):
    return input(prompt + " (y/n): ").strip().lower() == "y"


def pause():
    input("\nกด Enter เพื่อดำเนินการต่อ...")


# ---------- แสดงผล ----------
def money(value):
    return f"{float(value):,.2f}"


def _width(text):
    """ความกว้างตอนแสดงผล (สระ/วรรณยุกต์ไทยไม่นับความกว้าง)"""
    return sum(0 if unicodedata.category(c) == "Mn" else 1 for c in str(text))


def _fit(text, width, align="left"):
    """จัดข้อความให้พอดีความกว้าง: left / right / center"""
    gap = max(width - _width(text), 0)
    if align == "right":
        return " " * gap + str(text)
    if align == "center":
        left = gap // 2
        return " " * left + str(text) + " " * (gap - left)
    return str(text) + " " * gap


def _box_head(title, total):
    """หัวกล่อง: เส้นคู่ + ชื่อหัวข้อกึ่งกลาง + เส้นคู่"""
    print("=" * total)
    print("|" + _fit(title, total - 2, "center") + "|")
    print("=" * total)


def print_title(title, width=50):
    """หัวข้อหน้าจอ (ใช้กับหน้ากรอกข้อมูล)"""
    _box_head(title, max(width, _width(title) + 4))


def print_menu(title, items, width=50):
    """เมนูแบบกล่อง  items = list ของข้อความแต่ละบรรทัด"""
    total = max(width, _width(title) + 4, max(_width(i) for i in items) + 4)
    _box_head(title, total)
    for item in items:
        print("| " + _fit(item, total - 4) + " |")
    print("=" * total)


def print_table(title, headers, rows, right_cols=(), center_cols=(), footer=None):
    """ตารางแบบกล่อง
    right_cols  = คอลัมน์ที่ข้อมูลชิดขวา (เช่น ราคา)
    center_cols = คอลัมน์ที่ข้อมูลกึ่งกลาง (เช่น จำนวน)
    footer      = ข้อความสรุปท้ายตาราง
    """
    n = len(headers)
    widths = [max([_width(h)] + [_width(r[i]) for r in rows]) for i, h in enumerate(headers)]
    total = sum(widths) + 3 * n + 1
    need = max(_width(title), _width(footer) if footer else 0) + 4
    if need > total:                       # ขยายคอลัมน์สุดท้ายให้หัวข้อไม่ล้น
        widths[-1] += need - total
        total = need

    def align(i):
        return "right" if i in right_cols else "center" if i in center_cols else "left"

    _box_head(title, total)
    print("| " + " | ".join(
        _fit(h, widths[i], "center" if align(i) != "left" else "left")
        for i, h in enumerate(headers)) + " |")
    print("-" * total)
    if rows:
        for r in rows:
            print("| " + " | ".join(_fit(r[i], widths[i], align(i)) for i in range(n)) + " |")
    else:
        print("| " + _fit("(ไม่มีข้อมูล)", total - 4, "center") + " |")
    if footer:
        print("-" * total)
        print("| " + _fit(footer, total - 4) + " |")
    print("=" * total)
