from flask import Flask
from config import Config
from models import db, User, Employee, Department, Category, Product, Customer, Sale, SaleDetail
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config_class)
    
    # Veritabanı bağlantısı
    db.init_app(app)
    
    # Flask-Login ayarları
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Veritabanı migrasyon aracı
    migrate = Migrate(app, db)
    
    # Blueprint'leri kaydet
    from routes import main, auth, reports
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(reports)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)