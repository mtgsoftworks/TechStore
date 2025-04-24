from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Employee, Department, Product, Category, Sale, SaleDetail, Customer
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta

# Blueprint tanımlamaları
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')
reports = Blueprint('reports', __name__, url_prefix='/reports')

# Ana sayfa
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

# Dashboard sayfası
@main.route('/dashboard')
@login_required
def dashboard():
    # Temel istatistikleri getir
    total_sales = Sale.query.count()
    total_products = Product.query.count()
    total_customers = Customer.query.count()
    
    # Tarih bilgisini şablona aktar
    current_date = datetime.now()
    
    return render_template('dashboard.html', 
                           total_sales=total_sales,
                           total_products=total_products,
                           total_customers=total_customers,
                           current_date=current_date)

# Login sayfası
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!')
    
    return render_template('login.html')

# Çıkış yapma
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yapıldı.')
    return redirect(url_for('auth.login'))

# Rapor 1: Günlük satış miktarı
@reports.route('/daily-sales', methods=['GET', 'POST'])
@login_required
def daily_sales():
    # Varsayılan olarak bugünü kullan, istek yapılırsa belirli bir tarih kullan
    if request.method == 'POST' and request.form.get('date'):
        selected_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    # MS SQL Server için date() yerine CAST kullanımı
    daily_sales = db.session.query(
        func.sum(Sale.total_amount).label('total_amount')
    ).filter(
        cast(Sale.sale_date, Date) == selected_date
    ).scalar() or 0
    
    return render_template('daily_sales.html', daily_sales=daily_sales, date=selected_date)

# Rapor 2: Günlük en çok satılan ürün
@reports.route('/top-selling-product', methods=['GET', 'POST'])
@login_required
def top_selling_product():
    # Varsayılan olarak bugünü kullan, istek yapılırsa belirli bir tarih kullan
    if request.method == 'POST' and request.form.get('date'):
        selected_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()
    
    # MS SQL Server için date() yerine CAST kullanımı
    top_product = db.session.query(
        Product.id, Product.name, func.sum(SaleDetail.quantity).label('total_quantity')
    ).join(
        SaleDetail, SaleDetail.product_id == Product.id
    ).join(
        Sale, Sale.id == SaleDetail.sale_id
    ).filter(
        cast(Sale.sale_date, Date) == selected_date
    ).group_by(
        Product.id, Product.name
    ).order_by(
        func.sum(SaleDetail.quantity).desc()
    ).first()
    
    return render_template('top_selling_product.html', top_product=top_product, date=selected_date)

# Rapor 3: Personel maaş ve izin bilgileri
@reports.route('/employee-details')
@login_required
def employee_details():
    # Sadece yöneticilere izin ver
    if not current_user.is_admin:
        flash('Bu raporu görüntüleme yetkiniz yok!')
        return redirect(url_for('main.dashboard'))
    
    department_id = request.args.get('department_id', type=int)
    
    query = Employee.query.join(Department)
    
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    employees = query.all()
    departments = Department.query.all()
    
    return render_template('employee_details.html', 
                          employees=employees, 
                          departments=departments, 
                          selected_department=department_id)

# Ürün Yönetimi
@main.route('/products')
@login_required
def products():
    if not current_user.is_admin:
        abort(403)
    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/product/new', methods=['GET','POST'])
@login_required
def new_product():
    if not current_user.is_admin:
        abort(403)
    categories = Category.query.all()
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form.get('description'),
            price=request.form['price'],
            stock=request.form['stock'],
            category_id=request.form['category_id']
        )
        db.session.add(product)
        db.session.commit()
        flash('Ürün eklendi!')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', categories=categories)

@main.route('/product/edit/<int:product_id>', methods=['GET','POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        abort(403)
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form.get('description')
        product.price = request.form['price']
        product.stock = request.form['stock']
        product.category_id = request.form['category_id']
        db.session.commit()
        flash('Ürün güncellendi!')
        return redirect(url_for('main.products'))
    return render_template('product_form.html', product=product, categories=categories)

@main.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        abort(403)
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Ürün silindi!')
    return redirect(url_for('main.products'))

# Müşteri Yönetimi
@main.route('/customers')
@login_required
def customers():
    if not current_user.is_admin:
        abort(403)
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@main.route('/customer/new', methods=['GET','POST'])
@login_required
def new_customer():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        customer = Customer(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            phone=request.form.get('phone'),
            address=request.form.get('address')
        )
        db.session.add(customer)
        db.session.commit()
        flash('Müşteri eklendi!')
        return redirect(url_for('main.customers'))
    return render_template('customer_form.html')

@main.route('/customer/edit/<int:customer_id>', methods=['GET','POST'])
@login_required
def edit_customer(customer_id):
    if not current_user.is_admin:
        abort(403)
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.first_name = request.form['first_name']
        customer.last_name = request.form['last_name']
        customer.email = request.form['email']
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        db.session.commit()
        flash('Müşteri güncellendi!')
        return redirect(url_for('main.customers'))
    return render_template('customer_form.html', customer=customer)

@main.route('/customer/delete/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    if not current_user.is_admin:
        abort(403)
    # ensure customer exists
    customer = Customer.query.get_or_404(customer_id)
    # manual cascade deletion of details, sales, then customer
    SaleDetail.query.filter(
        SaleDetail.sale_id.in_(
            db.session.query(Sale.id).filter(Sale.customer_id == customer_id)
        )
    ).delete(synchronize_session=False)
    Sale.query.filter_by(customer_id=customer_id).delete(synchronize_session=False)
    Customer.query.filter_by(id=customer_id).delete(synchronize_session=False)
    db.session.commit()
    flash('Müşteri silindi!')
    return redirect(url_for('main.customers'))