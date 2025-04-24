from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    try:
        # Mevcut kullanıcıları bul
        admin = User.query.filter_by(username='admin').first()
        normal_user = User.query.filter_by(username='ahmet').first()
        
        # Şifreleri sıfırla
        if admin:
            admin.set_password('admin123')
            print(f"Admin kullanıcısının şifresi sıfırlandı: {admin.username}")
        else:
            print("Admin kullanıcısı bulunamadı!")
        
        if normal_user:
            normal_user.set_password('ahmet123')
            print(f"Normal kullanıcının şifresi sıfırlandı: {normal_user.username}")
        else:
            print("Normal kullanıcı bulunamadı!")

        # Değişiklikleri kaydet
        db.session.commit()
        print("Şifreler başarıyla güncellendi!")
    except Exception as e:
        print(f"Hata oluştu: {e}") 