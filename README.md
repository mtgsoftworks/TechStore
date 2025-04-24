# TechStore - Teknoloji Mağazası Yönetim Sistemi

Bu proje, bir teknoloji mağazasının envanter, satış, müşteri ilişkileri ve personel yönetimi işlemlerini gerçekleştiren bir web uygulamasıdır.

## Özellikler

- Ürün ve kategori yönetimi
- Stok takibi
- Satış işlemleri
- Müşteri veritabanı
- Personel yönetimi
- Satış ve performans raporları
- Kullanıcı yetkilendirme sistemi

## Kurulum

1. Projeyi klonlayın:
   ```
   git clone https://github.com/mtgsoftworks/techstore.git
   cd techstore
   ```

2. Sanal ortam oluşturun ve aktifleştirin:
   ```
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/MacOS
   source venv/bin/activate
   ```

3. Bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. `.env` dosyasını oluşturun:
   ```bash
   # Windows
   copy .env.example .env
   # Linux/MacOS
   cp .env.example .env
   ```
   Ve gerekli değişkenleri düzenleyin.

5. Microsoft SQL Server Kurulumu:
   - SQL Server'ın kurulu olduğundan emin olun
   - SQL Server Management Studio ile "techstoreDB" adlı bir veritabanı oluşturun
   - Windows kimlik doğrulaması kullanıldığından, ek kullanıcı ayarları gerekmez

6. Veritabanını oluşturun:
   ```
   flask db init
   flask db migrate -m "İlk migrasyon"
   flask db upgrade
   ```

7. Test verilerini ekleyin (opsiyonel):
   ```
   python test.py
   ```

8. Uygulamayı çalıştırın:
   ```bash
   # Windows
   python app.py
   # Linux/MacOS
   export FLASK_APP=app.py
   flask run
   ```

## Veritabanı Yapılandırması

Proje MS SQL Server kullanmaktadır:
- Server: DESKTOP-UC1QU5F\SQLEXPRESS
- Authentication: Windows Authentication
- Database: techstoreDB

Farklı bir veritabanı kullanmak için `config.py` dosyasını güncelleyin veya bir `.env` dosyasında `DATABASE_URL` değişkenini ayarlayın.

## Kullanım

Tarayıcıda http://localhost:5000 adresine gidin.
Varsayılan admin kullanıcısı:
- Kullanıcı adı: admin
- Şifre: admin123

## Dokümantasyon
- ER Diyagramı: [docs/ER_Diagram.puml](docs/ER_Diagram.puml)
- İş Kuralları: [docs/Is_Kurallari.md](docs/Is_Kurallari.md)
- Firma Tanıtımı: [docs/Firma_Tanitimi.md](docs/Firma_Tanitimi.md)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 