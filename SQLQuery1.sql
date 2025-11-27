USE Quan_Ly_Khach_San_Python;

CREATE TABLE Phong (
    MaPhong NVARCHAR(10) PRIMARY KEY,
    LoaiPhong NVARCHAR(40),
    TrangThai NVARCHAR(20),
    GiaTien INT
);

CREATE TABLE NhanVien (
    MaNV NVARCHAR(10) PRIMARY KEY,
    TenNV NVARCHAR(30),
    NgaySinh DATE,
    GioiTinh NVARCHAR(3) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    SoDienThoai CHAR(10) UNIQUE ,
    ChucVu NVARCHAR(40)
);

CREATE TABLE KhachHang (
    MaKH NVARCHAR(10) PRIMARY KEY,
    TenKH NVARCHAR(30),
    CCCD CHAR(12) UNIQUE,
    GioiTinh NVARCHAR(3) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    SoDienThoai CHAR(10) UNIQUE,
    QuocTich NVARCHAR(50)
);

CREATE TABLE DichVu (
    MaDV NVARCHAR(10) PRIMARY KEY,
    TenDV NVARCHAR(100),
    GiaDV INT
);

CREATE TABLE DatPhong (
    MaDatPhong INT IDENTITY(1,1) PRIMARY KEY,
    MaPhong NVARCHAR(10),
    MaKH NVARCHAR(10),
    TenKH NVARCHAR(30),
    NgayDat DATE,
    NgayNhan DATE,
    NgayTra DATE,
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (MaPhong) REFERENCES Phong(MaPhong),
);

CREATE TABLE ThanhToan (
    MaTT INT IDENTITY(1,1) PRIMARY KEY,
    MaDatPhong INT,
    NgayThanhToan DATE,
    TienPhong INT,
    TienDichVu INT,
    TongTien INT,
    FOREIGN KEY (MaDatPhong) REFERENCES DatPhong(MaDatPhong)
);

CREATE TABLE ChiTietDichVu (
    MaCTDV INT IDENTITY(1,1) PRIMARY KEY,
    MaDatPhong INT,
    MaDV NVARCHAR(10),
    SoLuong INT
    FOREIGN KEY (MaDatPhong) REFERENCES DatPhong(MaDatPhong),
    FOREIGN KEY (MaDV) REFERENCES DichVu(MaDV)
);

CREATE TABLE DangNhap (
    Username NVARCHAR(50) PRIMARY KEY,
    [Password] NVARCHAR(200) NOT NULL,
    MaNV NVARCHAR(10) UNIQUE,
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
);

INSERT INTO DangNhap (Username, [Password],MaNV) VALUES
('quan@admin','quan@admin','GD001'),
('tai@admin','tai@admin','GD002');
SELECT * FROM DangNhap

-- XOÁ 
DROP TABLE IF EXISTS ChiTietDichVu;
DROP TABLE IF EXISTS ThanhToan;
DROP TABLE IF EXISTS DatPhong;
DROP TABLE IF EXISTS DichVu;
DROP TABLE IF EXISTS KhachHang;
DROP TABLE IF EXISTS NhanVien;
DROP TABLE IF EXISTS Phong;


-- Xem thông tin
SELECT * FROM Phong
SELECT * FROM NhanVien
SELECT * FROM KhachHang
SELECT * FROM DichVu
SELECT * FROM Datphong
SELECT * FROM ChiTietDichVu
SELECT * FROM ThanhToan

DELETE FROM  Phong WHERE MaPhong = 'P001'
DELETE FROM  Phong WHERE MaPhong = 'P002'