# db_test.py
import pyodbc
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    # Ensure UTF-8 encoding for console output
    sys.stdout.reconfigure(encoding='utf-8')

try:
    # Veritabanı bağlantı bilgileri
    server = os.environ.get('DB_SERVER', 'localhost')
    port = os.environ.get('DB_PORT', '5820')
    database = os.environ.get('DB_DATABASE', 'techstoreDB')
    uid = os.environ.get('DB_USER', 'sa')
    pwd = os.environ.get('DB_PASSWORD', 'Your_password123')

    # SQL Authentication ile bağlantı
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={uid};PWD={pwd};TrustServerCertificate=yes;'

    # Bağlantıyı oluştur
    connection = pyodbc.connect(connection_string)
    # CREATE DATABASE requires autocommit mode
    connection.autocommit = True

    # Otomatik şema uygulama kaldırıldı; sadece test sorguları çalıştırılacak

    # Bağlantıyı başarılı mesajı
    print("SQL Server'a başarıyla bağlandı!")

    # Test sorgusu çalıştır - Users tablosundaki kullanıcıları listele
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, is_admin FROM Users")

    # Sonuçları yazdır
    print("\nKullanıcı Listesi:")
    print("ID\tKullanıcı Adı\tAdmin")
    print("-" * 30)

    for row in cursor:
        print(f"{row.id}\t{row.username}\t\t{row.is_admin}")

    # Departmanları kontrol et
    cursor.execute("SELECT id, name FROM Departments")

    print("\nDepartman Listesi:")
    print("ID\tDepartman Adı")
    print("-" * 20)

    for row in cursor:
        print(f"{row.id}\t{row.name}")

    # Bağlantıyı kapat
    connection.close()

except Exception as e:
    print(f"Hata: {e}")
    sys.exit(1)