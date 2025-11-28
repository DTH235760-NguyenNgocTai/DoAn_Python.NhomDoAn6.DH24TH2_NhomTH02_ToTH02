import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import datetime
from Form_QR import QRCode
from Form_Hoa_Don import HoaDon

class ThanhToan(tk.Toplevel):
    def __init__(self, parent=None, madp=None):
        super().__init__(parent)
        self.parent = parent
        self.madp = madp 
        self.title("THANH TOÁN")
        # Kích thước form
        window_width = 710
        window_height = 600

        self.transient(parent)
        self.grab_set()

        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Lấy vị trí ở giữa
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Đặt kích thước và vị trí
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.configure(bg="#000000")

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        self.Load_Database_CTDV()
        self.ThongTinThanhToan()
        self.TinhTien()

    # ============================= Kết nối Cơ Sở Dữ Liệu =============================
    def connect_database(self):
        try:
            conn = pyodbc.connect(
                r"DRIVER={ODBC Driver 17 for SQL Server};"
                r"SERVER=LAPTOP-VO3C4ONL;"
                r"DATABASE=Quan_Ly_Khach_San_Python;"
                r"Trusted_Connection=yes;"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối CSDL:\n{e}")
            return None

    # ----------------------------- Load Chi tiết dịch vụ -----------------------------
    def Load_Database_CTDV(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaCTDV, MaDatPhong, MaDV, SoLuong 
                          FROM ChiTietDichVu 
                          WHERE MaDatPhong = ?''', (self.madp,))
                       
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.ctdv.get_children():
            self.ctdv.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.ctdv.insert("", tk.END, values = clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    #  ----------------------------- Hiển thị thông tin thanh toán -----------------------------
    def ThongTinThanhToan(self):
        self.entry_madp.config(state = "normal")
        self.entry_madp.insert(0, self.madp)
        self.entry_madp.config(state = "readonly")

        self.entry_maphong.config(state = "normal")
        self.entry_makh.config(state = "normal")
        self.entry_tenkh.config(state = "normal")
        self.entry_loaiphong.config(state = "normal")
        self.entry_tienphong.config(state = "normal")

        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT dp.MaDatPhong, dp.MaPhong, dp.MaKH, kh.TenKH, p.LoaiPhong, p.GiaTien, dp.NgayNhan, dp.NgayTra
                                 FROM DatPhong dp
                                 JOIN KhachHang kh ON dp.MaKH = kh.MaKH
                                 JOIN Phong p ON dp.MaPhong = p.MaPhong
                                 WHERE dp.MaDatPhong = ?''', (self.madp,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin đặt phòng!")
            return

        # Lấy dữ liệu
        maphong = row[1]
        makh = row[2]
        tenkh = row[3]
        loaiphong = row[4]
        tienphong = row[5]
        ngaynhan = row[6]
        ngaytra = row[7]

        # Hiển thị thông tin lên entry
        self.entry_madp.insert(0, self.madp)
        self.entry_maphong.insert(0, maphong)
        self.entry_makh.insert(0,makh)
        self.entry_tenkh.insert(0, tenkh)
        self.entry_loaiphong.insert(0, loaiphong)
        self.entry_tienphong.insert(0, tienphong)
        # --- Ngày nhận và ngày trả ---
        try:
            # Nếu là chuỗi
            if isinstance(ngaynhan, str):
                try:
                    ngaynhan_dt = datetime.datetime.strptime(ngaynhan, "%Y-%m-%d").date()
                except:
                    ngaynhan_dt = datetime.datetime.strptime(ngaynhan, "%d/%m/%Y").date()
            else:
                ngaynhan_dt = ngaynhan  # đã là datetime.date

            if isinstance(ngaytra, str):
                try:
                    ngaytra_dt = datetime.datetime.strptime(ngaytra, "%Y-%m-%d").date()
                except:
                    ngaytra_dt = datetime.datetime.strptime(ngaytra, "%d/%m/%Y").date()
            else:
                ngaytra_dt = ngaytra  # đã là datetime.date

            self.ngaynhan.set_date(ngaynhan_dt)
            self.ngaytra.set_date(ngaytra_dt)

        except Exception as e:
            self.ngaynhan.set_date(datetime.date.today())
            self.ngaytra.set_date(datetime.date.today())

        self.entry_maphong.config(state = "readonly")
        self.entry_makh.config(state = "readonly")
        self.entry_tenkh.config(state = "readonly")
        self.entry_loaiphong.config(state = "readonly")
        self.entry_tienphong.config(state = "readonly")

    # ----------------------------- Tính Tiền -----------------------------
    def TinhTien(self):
        # --- Tiền phòng ---
        try:
            giaphong = int(self.entry_tienphong.get().strip())
        except:
            giaphong = 0
        
        try:
            ngay_nhan = self.ngaynhan.get_date()
            ngay_tra = self.ngaytra.get_date()
            songay = (ngay_tra - ngay_nhan).days + 1
        except:
            songay = 1

        tongtienphong = songay * giaphong
        self.entry_tongtienphong.config(state = "normal")
        self.entry_tongtienphong.delete(0, tk.END)
        self.entry_tongtienphong.insert(0, tongtienphong)
        self.entry_tongtienphong.config(state = "disabled")
        # --- Tiền dịch vụ ---
        tongtiendv = 0

        conn = self.connect_database()
        if conn:
            cursor = conn.cursor()
            for item in self.ctdv.get_children():
                row = self.ctdv.item(item, "values")
                madv = row[2]
                soluong = int(row[3])

                # Lấy giá DV
                cursor.execute("SELECT GiaDV FROM DichVu WHERE MaDV = ?", (madv,))
                result = cursor.fetchone()

                if result:
                    giadv = int(result[0])
                    tongtiendv += giadv * soluong
        conn.close()
        self.entry_tongtiendv.config(state = "normal")
        self.entry_tongtiendv.delete(0, tk.END)
        self.entry_tongtiendv.insert(0, tongtiendv)
        self.entry_tongtiendv.config(state = "disabled")

        # --- Thành tiền ---
        thanhtien = tongtienphong + tongtiendv
        self.entry_thanhtien.config(state = "normal")
        self.entry_thanhtien.delete(0, tk.END)
        self.entry_thanhtien.insert(0, thanhtien)
        self.entry_thanhtien.config(state = "disabled")
        
    # ----------------------------- Thanh Toán -----------------------------
    def ThanhToan_Click(self):
        self.rdbchuyenkhoan.config(state = "normal")
        self.rdbtienmat.config(state = "normal")
        self.btnChon.config(state = "normal")

    # ----------------------------- Chọn -----------------------------
    def Chon_Click(self):
        value = self.selected_option.get().strip()

        if value == "":
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phương thức thanh toán!")
            return

        madatphong = self.entry_madp.get().strip()
        tenkh = self.entry_tenkh.get().strip()
        maphong = self.entry_maphong.get().strip()
        loaiphong = self.entry_loaiphong.get().strip()
        giaphong = self.entry_tienphong.get().strip()
        tongtienphong = self.entry_tongtienphong.get().strip()
        tongtiendv = self.entry_tongtiendv.get().strip()
        thanhtien = self.entry_thanhtien.get().strip()

        # --- LẤY NGÀY HOÀN TOÀN ĐÚNG ---
        ngaynhan_dt = self.ngaynhan.get_date()
        ngaytra_dt = self.ngaytra.get_date()

        # Xác nhận
        result = messagebox.askyesno("Thông báo", f"Xác nhận thanh toán {value}?")
        if not result:
            return

        # --- Xử lý thanh toán ---
        try:
            if value == "Chuyển khoản":
                qr = QRCode(self)   # 1. mở form QR
                qr.grab_set()       # 2. khóa form cha (modal)
                self.wait_window(qr)  # 3. CHỜ ĐÓNG form QR trước khi chạy tiếp

                # 4. Form QR đóng thì mới mở hóa đơn
                HoaDon(self, madatphong, tenkh, maphong, loaiphong,
                        giaphong, tongtienphong, tongtiendv, thanhtien,
                        ngaynhan_dt, ngaytra_dt)
            else:  # tiền mặt
                HoaDon(self, madatphong, tenkh, maphong, loaiphong,
                       giaphong, tongtienphong, tongtiendv, thanhtien,
                       ngaynhan_dt, ngaytra_dt)

            # Mở nút đã thanh toán
            self.btnDathanhtoan.config(state="normal")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn:\n{e}")

    # ----------------------------- Đã thanh toán -----------------------------
    def DaThanhToan_Click(self):
        maphong = self.entry_maphong.get().strip()
        makh = self.entry_makh.get().strip()
        conn = self.connect_database()
        cursor = conn.cursor()
        # Xoa chi tiet dich vu
        cursor.execute("DELETE FROM ChiTietDichVu WHERE MaDatPhong = ?", (self.madp,))
        # Xoa thanh toan
        cursor.execute("DELETE FROM ThanhToan WHERE MaDatPhong = ?", (self.madp,))
        # Xoa dat phong
        cursor.execute("DELETE FROM DatPhong WHERE MaDatPhong = ?", (self.madp,))

        # Kiểm tra khách hàng còn đặt phòng nào khác không
        cursor.execute("SELECT COUNT(*) FROM DatPhong WHERE MaKH = ?", (makh,))
        countkh = cursor.fetchone()[0]

        if countkh == 0: # ko còn thì cập nhật / còn thì chỉ cập nhật phòng
            cursor.execute("DELETE FROM KhachHang WHERE MaKH = ?", (makh,))
        # cập nhật trạng thái phòng
        cursor.execute("UPDATE Phong SET TrangThai = ? WHERE MaPhong = ?", ("Trống", maphong))
        conn.commit()
        conn.close()

        messagebox.showinfo("Thông báo", "ĐÃ THANH TOÁN THÀNH CÔNG!")
        messagebox.showinfo("Thông báo", "Cảm ơn quý khách đã sử dụng khách sạn của chúng tôi!")

    # ----------------------------- Thoát -----------------------------        
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiển thị lại form cha
            self.destroy()    

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):

        # ----------------------------- Tên form -----------------------------
        title_label = tk.Label(self, text="THANH TOÁN",
                               font=("Arial", 20, "bold"),
                               fg="#FFAA78", bg="Black")
        title_label.place(relx = 0.5, y=5, anchor="n", width=700, height=40)

        # ----------------------------- Thông tin Thanh toán -----------------------------
        self.group_thongtin = tk.LabelFrame(self, text="Thông tin thanh toán",
                                            font=("Arial", 10),
                                            bg="#000000", fg="#0DFF00")
        self.group_thongtin.place(relx=0.005, rely=0.22, anchor="w", width=570, height=150)

        tk.Label(self.group_thongtin, text="Mã đặt phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_madp = tk.Entry(self.group_thongtin, state="disabled", font=("Arial", 10))
        self.entry_madp.place(x=120, y=5, width=160, height=20)

        tk.Label(self.group_thongtin, text="Mã phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_maphong = tk.Entry(self.group_thongtin, font=("Arial", 10))
        self.entry_maphong.place(x=120, y=35, width=160, height=20)

        tk.Label(self.group_thongtin, text="Mã khách hàng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_makh = tk.Entry(self.group_thongtin, font=("Arial", 10))
        self.entry_makh.place(x=120, y=65, width=160, height=20)

        tk.Label(self.group_thongtin, text="Tên khách hàng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=95)
        self.entry_tenkh = tk.Entry(self.group_thongtin, font=("Arial", 10))
        self.entry_tenkh.place(x=120, y=95, width=160, height=20)

        tk.Label(self.group_thongtin, text="Loại phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=310, y=5)
        self.entry_loaiphong = tk.Entry(self.group_thongtin, font=("Arial", 10))
        self.entry_loaiphong.place(x=380, y=5, width=160, height=20)

        tk.Label(self.group_thongtin, text="Tiền phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=310, y=35)
        self.entry_tienphong = tk.Entry(self.group_thongtin, font=("Arial", 10))
        self.entry_tienphong.place(x=380, y=35, width=160, height=20)

        tk.Label(self.group_thongtin, text="Ngày nhận", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=310, y=65)
        self.ngaynhan = DateEntry(self.group_thongtin, date_pattern="dd/mm/yyyy")
        self.ngaynhan.place(x=380, y=65, width=160, height=20)

        tk.Label(self.group_thongtin, text="Ngày trả", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=310, y=95)
        self.ngaytra = DateEntry(self.group_thongtin, date_pattern="dd/mm/yyyy")
        self.ngaytra.place(x=380, y=95, width=160, height=20)

        # ----------------------------- Phương thức thanh toán -----------------------------
        self.group_phuongthuc = tk.LabelFrame(self, text="Phương thức thanh toán",
                                             font=("Arial", 10), bg="#000000", fg="#0DFF00")
        self.group_phuongthuc.place(x=10, y=240, width=230, height=130)

        self.selected_option = tk.StringVar()
        self.rdbtienmat = tk.Radiobutton(self.group_phuongthuc, text="Tiền mặt", state = "disabled",
                                         variable=self.selected_option,
                                         value="Tiền mặt", font=("Arial", 10),
                                         fg="#FCBD00", bg="#000000")
        self.rdbchuyenkhoan = tk.Radiobutton(self.group_phuongthuc, text="Chuyển khoản", state = "disabled",
                                         variable=self.selected_option,
                                         value="Chuyển khoản", font=("Arial", 10),
                                         fg="#FCBD00", bg="#000000")

        self.rdbtienmat.place(x=10, y=10)
        self.rdbchuyenkhoan.place(x=10, y=40)

        self.btnChon = tk.Button(self.group_phuongthuc, text="Chọn", state = "disabled",
                                 font=("Arial", 12),
                                 fg="#000000", bg="#0DFF00", command = self.Chon_Click)
        self.btnChon.place(x=120, y=20, width=90, height=40)

        # ----------------------------- Chi phí -----------------------------
        self.group_chiphi = tk.LabelFrame(self, text="Thông tin chi phí", font=("Arial", 10),
                                      bg="#000000", fg="#0DFF00")
        self.group_chiphi.place(x=250, y=220, width=325, height=120)

        tk.Label(self.group_chiphi, text="Tổng tiền phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=5)
        self.entry_tongtienphong = tk.Entry(self.group_chiphi, font=("Arial", 10), state = "readonly")
        self.entry_tongtienphong.place(x=120, y=5, width=160, height=20)

        tk.Label(self.group_chiphi, text="Tổng tiền dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=35)
        self.entry_tongtiendv = tk.Entry(self.group_chiphi, font=("Arial", 10), state = "readonly")
        self.entry_tongtiendv.place(x=120, y=35, width=160, height=20)

        tk.Label(self.group_chiphi, text="Thành tiền", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=65)
        self.entry_thanhtien = tk.Entry(self.group_chiphi, font=("Arial", 10), state = "readonly")
        self.entry_thanhtien.place(x=120, y=65, width=160, height=20)

        # ----------------------------- Bảng Chi tiết dịch vụ -----------------------------
        frame_ctdv = tk.Frame(self, bg="black")
        frame_ctdv.place(x=10, y=350, width=600, height=150)

        self.ctdv = ttk.Treeview(frame_ctdv,
                                 columns=("MaCTDV", "MaDatPhong", "MaDV", "SoLuong"),
                                 show="headings")

        scroll_y = tk.Scrollbar(frame_ctdv, orient="vertical", command=self.ctdv.yview)
        scroll_x = tk.Scrollbar(frame_ctdv, orient="horizontal", command=self.ctdv.xview)
        self.ctdv.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.ctdv.pack(fill="both", expand=True)

        self.ctdv.heading("MaCTDV", text="Mã CTDV")
        self.ctdv.heading("MaDatPhong", text="Mã đặt phòng")
        self.ctdv.heading("MaDV", text="Mã dịch vụ")
        self.ctdv.heading("SoLuong", text="Số lượng")

        self.ctdv.column("MaCTDV", width=80)
        self.ctdv.column("MaDatPhong", width=150)
        self.ctdv.column("MaDV", width=150)
        self.ctdv.column("SoLuong", width=100)

        # ----------------------------- Buttons -----------------------------
        self.btnThanhtoan = tk.Button(self, text="Thanh toán", font=("Arial", 12),
                                      fg="white", bg="#001f4d", command = self.ThanhToan_Click)
        self.btnThanhtoan.place(x=580, y=70, width=120, height=30)

        self.btnDathanhtoan = tk.Button(self, text="Đã thanh toán", font=("Arial", 12),
                                        fg="white", bg="#001f4d", command = self.DaThanhToan_Click)
        self.btnDathanhtoan.place(x=580, y=110, width=120, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                                  fg="white", bg="#001f4d", command=self.Thoat_Click)
        self.btnThoat.place(x=580, y=150, width=120, height=30)