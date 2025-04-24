import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()
# .env dosyası yoksa .env.example dosyasını yükle
load_dotenv('.env.example', override=False)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    # Ortam değişkenlerinden varsayılan bağlantı parametrelerini al
    db_server   = os.environ.get('DB_SERVER',   'localhost')
    db_port     = os.environ.get('DB_PORT',     '5820')
    db_user     = os.environ.get('DB_USER',     'sa')
    db_password = os.environ.get('DB_PASSWORD', 'Your_password123')
    db_database = os.environ.get('DB_DATABASE', 'techstoreDB')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f"mssql+pyodbc://{db_user}:{db_password}@{db_server},{db_port}/{db_database}"
        "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # SQL sorgularını konsola yazdırır, hata ayıklama için