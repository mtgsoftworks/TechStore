"""
sql_test.py

Scripts to validate database operations for your company project.
Requires: pyodbc (pip install pyodbc)
Configure connection settings below.
"""

import pyodbc
import os

# --- BAĞLANTI AYARLARI ---
SERVER = os.environ.get('DB_SERVER', 'localhost,5820')       # Sunucu,port
database = os.environ.get('DB_DATABASE', 'techstoreDB')      # Veritabanı adı
UID = os.environ.get('DB_USER', 'sa')                        # SQL kullanıcı adı
PWD = os.environ.get('DB_PASSWORD', 'Your_password123')      # SQL şifresi
DRIVER = '{ODBC Driver 17 for SQL Server}'
TRUST_SERVER_CERT = 'yes'                                    # Sertifika onayı


def get_connection():
    conn_str = (
        f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={database};"
        f"UID={UID};PWD={PWD};TrustServerCertificate={TRUST_SERVER_CERT};"
    )
    return pyodbc.connect(conn_str)


def test_insert_update_delete():
    print('== Ekleme-Güncelleme-Silme Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    name = input('Ürün adı: ')
    price = float(input('Fiyat: '))
    category_id = int(input('Kategori id: '))
    # Ürün ekle ve id al
    cur.execute(
        "INSERT INTO Products (name, price, category_id) OUTPUT INSERTED.id VALUES (?, ?, ?)",
        (name, price, category_id)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    print(f'Ürün eklendi: id={new_id}')
    new_price = float(input('Yeni fiyat: '))
    cur.execute("UPDATE Products SET price = ? WHERE id = ?", (new_price, new_id))
    conn.commit()
    print(f'Ürün güncellendi: id={new_id}')
    confirm = input(f"{new_id} id'li ürünü silmek istiyor musunuz? (e/h): ")
    if confirm.lower() == 'e':
        cur.execute("DELETE FROM Products WHERE id = ?", (new_id,))
        conn.commit()
        print(f'Ürün silindi: id={new_id}')
    cur.close()
    conn.close()


def test_view():
    print('== Görünüm Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    view_name = input('Görünüm adı (MonthlyTotalSales varsayılan): ') or 'MonthlyTotalSales'
    if view_name.lower() == 'monthlytotalsales':
        year = input('Yıl (YYYY, boş bırak tüm yıl): ')
        month = input('Ay (MM, boş bırak tüm ay): ')
        if year and month:
            cur.execute(f"SELECT * FROM {view_name} WHERE sale_year = ? AND sale_month = ?", (year, month))
        else:
            cur.execute(f"SELECT * FROM {view_name}")
    else:
        cur.execute(f"SELECT * FROM {view_name}")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


def test_stored_procedure():
    print('== Stored Procedure Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    # Kullanıcıdan tarih aralığı al
    start_date = input('Başlangıç tarihi (YYYY-MM-DD): ')
    end_date = input('Bitiş tarihi (YYYY-MM-DD): ')
    cur.execute("EXEC GetSalesByDateRange @StartDate = ?, @EndDate = ?", (start_date, end_date))
    print(f"Tarihler: {start_date} - {end_date}")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


def test_trigger():
    print('== Trigger Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    # Kullanıcıdan parametreleri al
    prod_id = int(input('Ürün id: '))
    cust_id = int(input('Müşteri id: '))
    emp_id = int(input('Çalışan id: '))
    qty = int(input('Satış adedi: '))
    unit_price = float(input('Birim fiyat: '))
    # Ürün için mevcut stok değerini al
    cur.execute("SELECT stock FROM Products WHERE id = ?", (prod_id,))
    orig_stock = cur.fetchone()[0]
    # Yeni satış kaydı ekle (trigger tetiklenecek)
    cur.execute("INSERT INTO Sales (customer_id, employee_id, total_amount) OUTPUT INSERTED.id VALUES (?, ?, ?)", (cust_id, emp_id, qty*unit_price))
    sale_id = cur.fetchone()[0]
    conn.commit()
    # Satış detayı ekle, trigger stok güncelleyecek
    cur.execute("INSERT INTO SaleDetails (sale_id, product_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)", (sale_id, prod_id, qty, unit_price, qty*unit_price))
    conn.commit()
    # Güncellenmiş stok değerini al
    cur.execute("SELECT stock FROM Products WHERE id = ?", (prod_id,))
    new_stock = cur.fetchone()[0]
    print(f"Stok değeri: {orig_stock} -> {new_stock}")
    # Temizlik: test kayıtlarını sil ve eski stoğu geri yükle
    cur.execute("DELETE FROM SaleDetails WHERE sale_id = ?", (sale_id,))
    cur.execute("DELETE FROM Sales WHERE id = ?", (sale_id,))
    cur.execute("UPDATE Products SET stock = ? WHERE id = ?", (orig_stock, prod_id))
    conn.commit()
    cur.close()
    conn.close()


def test_login(username, password):
    print('== Login Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    # Kullanıcı adı/şifre kontrolü (plain-text şifre)
    cur.execute("SELECT CASE WHEN EXISTS (SELECT 1 FROM Users WHERE username=? AND password_hash=?) THEN 1 ELSE 0 END", (username, password))
    success = cur.fetchone()[0]
    print('Login', 'successful' if success else 'failed')
    cur.close()
    conn.close()


def test_reports():
    print('== Rapor Testi ==')
    conn = get_connection()
    cur = conn.cursor()
    report_date = input('Rapor tarihi (YYYY-MM-DD, boş bırak bugün): ')
    if report_date:
        cur.execute("SELECT SUM(total_amount) FROM Sales WHERE CAST(sale_date AS DATE) = ?", (report_date,))
    else:
        cur.execute("SELECT SUM(total_amount) FROM Sales WHERE CAST(sale_date AS DATE) = CAST(GETDATE() AS DATE)")
    print('Günlük Satış:', cur.fetchone()[0])
    # Report 2: En çok satılan ürün
    cur.execute("""
        SELECT TOP 1 p.name, SUM(sd.quantity) AS total_qty
        FROM SaleDetails sd
        JOIN Sales s ON sd.sale_id=s.id
        JOIN Products p ON sd.product_id=p.id
        GROUP BY p.name
        ORDER BY total_qty DESC
    """)
    top = cur.fetchone()
    print('En Çok Satılan:', top)
    # Report 3: Çalışan maaş ve yıllık izin bilgisi
    cur.execute("SELECT first_name, last_name, salary, annual_leave FROM Employees")
    print('Çalışan Maaş & Yıllık İzin:')
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()


if __name__ == '__main__':
    while True:
        print("\n--- SQL Test Menüsü ---")
        print("1. Ekleme-Güncelleme-Silme Testi")
        print("2. Görünüm Testi")
        print("3. Stored Procedure Testi")
        print("4. Trigger Testi")
        print("5. Login Testi")
        print("6. Rapor Testi")
        print("0. Çıkış")
        secim = input("Seçiminiz: ")
        if secim == '1':
            test_insert_update_delete()
        elif secim == '2':
            test_view()
        elif secim == '3':
            test_stored_procedure()
        elif secim == '4':
            test_trigger()
        elif secim == '5':
            username = input("Kullanıcı adı: ")
            password = input("Şifre: ")
            test_login(username, password)
        elif secim == '6':
            test_reports()
        elif secim == '0':
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçim, tekrar deneyin.")
