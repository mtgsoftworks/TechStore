from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# Kategori Tablosu
class Category(db.Model):
    __tablename__ = 'Categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=True)
    
    # Hiyerarşik yapı için ilişkiler
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    products = db.relationship('Product', backref='category', lazy=True)

# Ürün Tablosu
class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sale_details = db.relationship('SaleDetail', backref='product', lazy=True)

# Departman Tablosu
class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    employees = db.relationship('Employee', backref='department', lazy=True)

# Çalışan Tablosu
class Employee(db.Model):
    __tablename__ = 'Employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    annual_leave = db.Column(db.Integer, default=14)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'), nullable=False)
    
    sales = db.relationship('Sale', backref='employee', lazy=True)

# Müşteri Tablosu
class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sales = db.relationship('Sale', backref='customer', lazy=True)

# Satış Tablosu
class Sale(db.Model):
    __tablename__ = 'Sales'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    sale_details = db.relationship('SaleDetail', backref='sale', lazy=True, cascade="all, delete-orphan")

# Satış Detay Tablosu
class SaleDetail(db.Model):
    __tablename__ = 'SaleDetails'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('Sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

# Kullanıcı Tablosu (Login için)
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.id'), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    employee = db.relationship('Employee', backref='user_account', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # support both hashed and plain-text passwords
        if self.password_hash and self.password_hash.startswith('pbkdf2:'):
            return check_password_hash(self.password_hash, password)
        return self.password_hash == password
    
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)