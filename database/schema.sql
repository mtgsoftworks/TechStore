-- Veritabanını oluştur
CREATE DATABASE techstoreDB;
GO

USE techstoreDB;
GO

-- Kategori Tablosu
CREATE TABLE Categories (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    parent_id INT NULL
);
GO

-- Kategori self-referencing kısıtlaması
ALTER TABLE Categories
ADD CONSTRAINT FK_Categories_Categories FOREIGN KEY (parent_id) REFERENCES Categories(id);
GO

-- Departman Tablosu
CREATE TABLE Departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL
);
GO

-- Çalışan Tablosu
CREATE TABLE Employees (
    id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    annual_leave INT DEFAULT 14,
    department_id INT NOT NULL,
    CONSTRAINT FK_Employees_Departments FOREIGN KEY (department_id) REFERENCES Departments(id)
);
GO

-- Müşteri Tablosu
CREATE TABLE Customers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    phone NVARCHAR(20) NULL,
    address NVARCHAR(MAX) NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Kullanıcı Tablosu
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(256) NOT NULL,
    employee_id INT NULL,
    is_admin BIT DEFAULT 0,
    CONSTRAINT FK_Users_Employees FOREIGN KEY (employee_id) REFERENCES Employees(id)
);
GO

-- Ürün Tablosu
CREATE TABLE Products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX) NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    category_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (category_id) REFERENCES Categories(id)
);
GO

-- Satış Tablosu
CREATE TABLE Sales (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_id INT NOT NULL,
    sale_date DATETIME DEFAULT GETDATE(),
    total_amount DECIMAL(10, 2) NOT NULL,
    CONSTRAINT FK_Sales_Customers FOREIGN KEY (customer_id) REFERENCES Customers(id),
    CONSTRAINT FK_Sales_Employees FOREIGN KEY (employee_id) REFERENCES Employees(id)
);
GO

-- Satış Detay Tablosu
CREATE TABLE SaleDetails (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT FK_SaleDetails_Sales FOREIGN KEY (sale_id) REFERENCES Sales(id),
    CONSTRAINT FK_SaleDetails_Products FOREIGN KEY (product_id) REFERENCES Products(id)
);
GO

-- View: Aylık Satış Özeti
CREATE VIEW MonthlyTotalSales AS
SELECT 
    YEAR(sale_date) as sale_year,
    MONTH(sale_date) as sale_month,
    SUM(total_amount) as monthly_total
FROM Sales
GROUP BY YEAR(sale_date), MONTH(sale_date);
GO

-- Stored Procedure: Belirli bir tarih aralığındaki satışlar
CREATE PROCEDURE GetSalesByDateRange
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN
    SELECT s.id, s.sale_date, c.first_name + ' ' + c.last_name as customer_name,
           e.first_name + ' ' + e.last_name as employee_name,
           s.total_amount
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.id
    JOIN Employees e ON s.employee_id = e.id
    WHERE s.sale_date BETWEEN @StartDate AND @EndDate
    ORDER BY s.sale_date DESC;
END;
GO

-- Trigger: Satış yapıldığında stok güncelleme
CREATE TRIGGER trg_UpdateStock
ON SaleDetails
AFTER INSERT
AS
BEGIN
    UPDATE p
    SET p.stock = p.stock - i.quantity
    FROM Products p
    JOIN inserted i ON p.id = i.product_id;
END;
GO

-- 1. Departmanlar
INSERT INTO Departments (name) VALUES 
('Satış'),
('Depo'),
('Yönetim');
GO

-- 2. Çalışanlar
INSERT INTO Employees (first_name, last_name, email, hire_date, salary, annual_leave, department_id) VALUES 
('Ahmet', 'Yılmaz', 'ahmet@techstore.com', '2023-01-15', 12000, 14, 1),
('Ayşe', 'Demir', 'ayse@techstore.com', '2022-05-10', 11000, 21, 2),
('Mehmet', 'Kaya', 'mehmet@techstore.com', '2021-03-20', 18000, 28, 3),
('Elif', 'Çelik', 'elif@techstore.com', '2024-02-01', 10000, 14, 1),
('Fatih', 'Demir', 'fatih@techstore.com', '2023-11-20', 9000, 14, 2);
GO

-- 3. Kullanıcılar (örnek şifrelerle)
INSERT INTO Users (username, password_hash, employee_id, is_admin) VALUES 
('admin', 'admin', 3, 1),
('ahmet', 'ahmet', 1, 0),
('elif', 'elif', 4, 0),
('fatih', 'fatih', 5, 0);
GO

-- 4. Kategori hiyerarşisi ve ürünler
-- Ana kategori
INSERT INTO Categories (name, parent_id) VALUES ('Elektronik', NULL);
DECLARE @elektronikId INT = SCOPE_IDENTITY();

-- Alt kategoriler (birinci seviye)
INSERT INTO Categories (name, parent_id) VALUES ('Bilgisayarlar', @elektronikId);
DECLARE @bilgisayarlarId INT = SCOPE_IDENTITY();

INSERT INTO Categories (name, parent_id) VALUES ('Telefonlar', @elektronikId);
DECLARE @telefonlarId INT = SCOPE_IDENTITY();

-- Alt kategoriler (ikinci seviye)
INSERT INTO Categories (name, parent_id) VALUES ('Dizüstü Bilgisayarlar', @bilgisayarlarId);
DECLARE @dizustuId INT = SCOPE_IDENTITY();

INSERT INTO Categories (name, parent_id) VALUES ('Masaüstü Bilgisayarlar', @bilgisayarlarId);
DECLARE @masaustuId INT = SCOPE_IDENTITY();

-- Aksesuarlar kategorisi
INSERT INTO Categories (name, parent_id) VALUES ('Aksesuarlar', @elektronikId);
DECLARE @aksesuarlarId INT = SCOPE_IDENTITY();

-- Tablet kategorisi
INSERT INTO Categories (name, parent_id) VALUES ('Tablet', @elektronikId);
DECLARE @tabletId INT = SCOPE_IDENTITY();

INSERT INTO Categories (name, parent_id) VALUES ('Akıllı Telefonlar', @telefonlarId);
DECLARE @akilliTelefonlarId INT = SCOPE_IDENTITY();

-- 5. Ürünler
INSERT INTO Products (name, description, price, stock, category_id) VALUES 
('HP Pavilion', '15.6 inç Dizüstü Bilgisayar', 12999.99, 25, @dizustuId),
('Dell XPS', '13 inç Dizüstü Bilgisayar', 17499.99, 15, @dizustuId),
('Lenovo ThinkPad', '14 inç Dizüstü Bilgisayar', 15499.99, 20, @dizustuId),
('Asus ROG Strix', 'Oyun Masaüstü Bilgisayar', 21999.99, 10, @masaustuId),
('Apple iMac', '24 inç All-in-One Masaüstü', 23999.99, 8, @masaustuId),
('iPhone 14', '128GB Akıllı Telefon', 25999.99, 30, @akilliTelefonlarId),
('Samsung Galaxy S23', '256GB Akıllı Telefon', 19999.99, 40, @akilliTelefonlarId),
('iPad Pro', '12.9 inç Tablet', 22999.99, 25, @tabletId),
('Logitech Kablosuz Mouse', 'Kablosuz Optik Mouse', 299.99, 100, @aksesuarlarId),
('Razer Mekanik Klavye', 'Mekanik Oyun Klavye', 999.99, 50, @aksesuarlarId),
('Dell 24 Monitör', '24 inç Full HD Monitör', 1999.99, 30, @aksesuarlarId);
GO

-- 6. Müşteriler
INSERT INTO Customers (first_name, last_name, email, phone) VALUES 
('Ali', 'Öztürk', 'ali@example.com', '5551234567'),
('Zeynep', 'Şahin', 'zeynep@example.com', '5559876543'),
('Can', 'Kara', 'can@example.com', '5551112222'),
('Selin', 'Yıldız', 'selin@example.com', '5553334444'),
('Mert', 'Aydın', 'mert@example.com', '5555556666');
GO

-- Örnek Satış Verileri
DECLARE @s1 INT, @s2 INT, @s3 INT;
INSERT INTO Sales (customer_id, employee_id, total_amount) VALUES (1, 1, 26299.98);
SET @s1 = SCOPE_IDENTITY();
INSERT INTO Sales (customer_id, employee_id, total_amount) VALUES (2, 2, 39999.98);
SET @s2 = SCOPE_IDENTITY();
INSERT INTO Sales (customer_id, employee_id, total_amount) VALUES (3, 4, 24999.97);
SET @s3 = SCOPE_IDENTITY();

-- Örnek Satış Detayları
INSERT INTO SaleDetails (sale_id, product_id, quantity, unit_price, subtotal) VALUES
    (@s1, 6, 1, 25999.99, 25999.99),
    (@s1, 9, 1, 299.99, 299.99),
    (@s2, 7, 2, 19999.99, 39999.98),
    (@s3, 8, 1, 22999.99, 22999.99),
    (@s3, 10, 2, 999.99, 1999.98);
GO

-- View: En Çok Satan Ürünler
CREATE VIEW TopSellingProducts AS
SELECT p.id AS product_id,
       p.name AS product_name,
       SUM(sd.quantity) AS total_sold
FROM SaleDetails sd
JOIN Products p ON sd.product_id = p.id
GROUP BY p.id, p.name
ORDER BY SUM(sd.quantity) DESC;
GO

-- View: Personel Maaş ve Yıllık İzin Raporu
CREATE VIEW EmployeeSalaryLeave AS
SELECT e.id AS employee_id,
       e.first_name + ' ' + e.last_name AS employee_name,
       e.salary,
       e.annual_leave
FROM Employees e;
GO

-- Stored Procedure: Personel Maaş ve İzin Raporu
CREATE PROCEDURE GetEmployeeSalaryReport
AS
BEGIN
    SELECT e.id AS employee_id,
           e.first_name + ' ' + e.last_name AS employee_name,
           e.salary,
           e.annual_leave
    FROM Employees e;
END;
GO

-- Örnek UPDATE Komutu: Çalışanın maaşını %10 artır
UPDATE Employees
SET salary = salary * 1.10
WHERE id = 1;
GO

-- Örnek DELETE Komutu: Müşteri kaydını sil
DELETE FROM Customers
WHERE id = 5;
GO

PRINT 'Veritabanı ve örnek veriler başarıyla oluşturuldu!';