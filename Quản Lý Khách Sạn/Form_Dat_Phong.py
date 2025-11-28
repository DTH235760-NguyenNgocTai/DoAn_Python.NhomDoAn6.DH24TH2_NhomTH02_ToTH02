import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import datetime
from Form_Dat_Dich_Vu import DatDichVu

class DatPhong(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)   # Gọi constructor của Toplevel
        self.parent = parent
        self.title("ĐẶT PHÒNG")
        self.window_width = 900
        self.window_height = 600
        self.transient(parent)
        self.grab_set()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.configure(bg="#000000")

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        self.Load_Database_Phong()
        self.Load_Database_DatPhong()

    # ============================= Kết nối Database =============================
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

    # ============================= Load dữ liệu bảng Phòng & Đặt Phòng =============================
    def Dinhdangtien(value):
        return f"{value:,.0f} đ".replace(",", ".")
    
    def Load_Database_Phong(self):
        conn = self.connect_database()
        if conn is None:
            return
    
        cursor = conn.cursor()
        cursor.execute('''SELECT MaPhong, LoaiPhong, TrangThai, GiaTien 
                      FROM Phong
                      WHERE TrangThai = ?''', ("Trống",))
        rows = cursor.fetchall()

    # Xóa dữ liệu cũ
        for i in self.phong.get_children():
            self.phong.delete(i)

    # Thêm dữ liệu mới
        for row in rows:
            ma, loai, trangthai, giatien = row
        
        # Format tiền tệ
            giatien_fmt = f"{giatien:,.0f} ₫".replace(",", ".")

            clean_row = [ma, loai, trangthai, giatien_fmt]

            self.phong.insert("", tk.END, values=clean_row)

        conn.close()
    
    # =================== Load dữ liệu Đặt Phòng ===================
    def Load_Database_DatPhong(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DatPhong")
        rows = cursor.fetchall()

        for item in self.datphong.get_children():
            self.datphong.delete(item)

        for madp, maphong, makh, tenkh, ngaydat, ngaynhan, ngaytra in rows:

            # Format ngày từ datetime → dd/mm/yyyy
            ngaydat  = ngaydat.strftime("%d/%m/%Y")
            ngaynhan = ngaynhan.strftime("%d/%m/%Y")
            ngaytra  = ngaytra.strftime("%d/%m/%Y")

            clean_row = [
                madp, maphong, makh, tenkh,
                ngaydat, ngaynhan, ngaytra
            ]

            self.datphong.insert("", tk.END, values=clean_row)

        conn.close()
    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()
    
    def on_child_close(self, child):
        # Khi form con đóng, form cha mới xuất hiện lại
        child.destroy()
        self.deiconify()
            
    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # ============================= ClearInput =============================
    def ClearInput(self):
        self.entry_madp.config(state="normal")  # Luôn đóng (Ko cho nhập)
        self.entry_madp.delete(0, tk.END)
        self.entry_madp.config(state="readonly")

        self.entry_maphong.config(state="normal")
        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")
        self.entry_cccd.config(state="normal")
        self.entry_sdt.config(state="normal")
        self.entry_quoctich.config(state="normal")

        self.entry_maphong.delete(0, tk.END)
        self.entry_makh.delete(0, tk.END)
        self.entry_tenkh.delete(0, tk.END)
        self.entry_cccd.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_quoctich.delete(0, tk.END)
        self.selected_option.set("")
        self.ngaydat.set_date(datetime.date.today())
        self.ngaynhan.set_date(datetime.date.today())
        self.ngaytra.set_date(datetime.date.today())

    def convert_date(self, sql_date):
    # Nếu đã là object datetime.date thì dùng luôn
        if isinstance(sql_date, datetime.date):
            return sql_date

        sql_date = str(sql_date).strip()

        # Chuẩn dd/mm/yyyy
        try:
            return datetime.datetime.strptime(sql_date, "%d/%m/%Y").date()
        except:
            return datetime.date.today()
        
    def Chon_Dong_Phong(self, event):
        # Lấy dòng đang được chọn
        selected = self.phong.selection()
        if selected:
            item = self.phong.item(selected[0])["values"]

            self.entry_maphong.config(state="normal")
            self.entry_maphong.delete(0, tk.END)
            self.entry_maphong.insert(0, item[0])
            self.entry_maphong.config(state="readonly")

            # Nếu phòng đang "Đã đặt" thì không cho đặt tiếp (bị thừa)
            if item[2] == "Đã đặt trước":
                messagebox.showwarning("Phòng đã được đặt", "Phòng này đã có khách! Vui lòng chọn phòng khác.")
                self.entry_maphong.config(state="normal")
                self.entry_maphong.delete(0, tk.END)
                return

    def Chon_Dong_DatPhong(self, event):
        selected = self.datphong.selection()
        if selected:
            item = self.datphong.item(selected[0])["values"]

            self.entry_madp.config(state="normal")
            self.entry_madp.delete(0, tk.END)
            self.entry_madp.insert(0, item[0])
            self.entry_madp.config(state="disabled")

            self.entry_maphong.config(state="normal")
            self.entry_maphong.delete(0, tk.END)
            self.entry_maphong.insert(0, item[1])
            self.entry_maphong.config(state="readonly")

            self.entry_makh.config(state="normal")
            self.entry_makh.delete(0, tk.END)
            self.entry_makh.insert(0, item[2])
            self.entry_makh.config(state="readonly")

            self.entry_tenkh.config(state="normal")
            self.entry_tenkh.delete(0, tk.END)
            self.entry_tenkh.insert(0, item[3])
            self.entry_tenkh.config(state="readonly")

            self.ngaydat.set_date(self.convert_date(item[4]))
            self.ngaynhan.set_date(self.convert_date(item[5]))
            self.ngaytra.set_date(self.convert_date(item[6]))

        # ---Kiểm tra Số điện thoại ---
    def Check_Sdt(self, sdt):
        if len(sdt) == 10 and sdt.isdigit():
            return True
        else:
            return False
        
    # --- Kiểm tra CCCD
    def Check_Cccd(self, cccd):
        if len(cccd) == 12 and cccd.isdigit():
            return True
        else:
            return False

    # --- Kiểm tra ngày đặt nhận trả ---    
    def Check_Ngay(self, ngaydat: str, ngaynhan: str, ngaytra: str):
        date_dat = datetime.datetime.strptime(ngaydat, "%d/%m/%Y").date()
        date_nhan = datetime.datetime.strptime(ngaynhan, "%d/%m/%Y").date()
        date_tra  = datetime.datetime.strptime(ngaytra, "%d/%m/%Y").date()
        # Kiểm tra 
        if date_nhan < date_dat:
            return "Ngày nhận phải sau hoặc bằng ngày đặt."
        if date_tra <= date_nhan:
            return "Ngày trả phải sau ngày nhận."
        return True

    # ============================= Nhập thông tin =============================    
    def NhapThongTin_Click(self):
        self.ClearInput()
        # Chọn dòng ở bảng phòng
        selected_phong = self.phong.selection()
        if not selected_phong:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần đặt!")
            return
        
        # Lấy thông tin phòng đưa lên entry
        item_phong = self.phong.item(selected_phong[0])["values"]
        self.entry_maphong.delete(0, tk.END)
        self.entry_maphong.insert(0, item_phong[0])
        self.entry_makh.focus_set()
        self.btnDat.config(state = "normal")
        self.btnHuy.config(state = "normal")

    # ============================= Đặt phòng =============================
    def Dat_Click(self):
        maphong = self.entry_maphong.get().strip()
        makh = self.entry_makh.get().strip()
        tenkh = self.entry_tenkh.get().strip()
        cccd = self.entry_cccd.get().strip()
        gioitinh = self.selected_option.get().strip()
        sdt = self.entry_sdt.get().strip()
        quoctich = self.entry_quoctich.get().strip()

        ngaydat = self.ngaydat.get_date()  # Lấy ngày từ DateEntry
        ngaynhan = self.ngaynhan.get_date()
        ngaytra = self.ngaytra.get_date()

        if not maphong:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần đặt!")
            return        

        if not makh or not tenkh or not cccd or not gioitinh or not sdt or not quoctich:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin khách hàng!")
            return
        
        if not ngaydat or not ngaynhan or not ngaytra:
            messagebox.showwarning("Thông báo", "Vui lòng nhập ngày đặt-nhận-trả phòng!")
            return

        if not self.Check_Sdt(sdt):
            messagebox.showerror("Lỗi", "Số điện thoại phải là số và có đúng 10 chữ số!")
            return
        
        if not self.Check_Cccd(cccd):
            messagebox.showerror("Lỗi", "CCCD phải là số và có đúng 12 chữ số!")
            return
        
        result = messagebox.askyesno("Xác nhận", f"Bạn có muốn đặt phòng {maphong} không?")
        if not result:
            return
        conn = self.connect_database()
        cursor = conn.cursor()
        # --- Thêm thông tin cho bảng khách hàng ---
        try:
            cursor.execute(
                "INSERT INTO KhachHang VALUES (?, ?, ?, ?, ?, ?)",
                (makh, tenkh, cccd, gioitinh, sdt, quoctich)
            )
            conn.commit()
            messagebox.showinfo("Thông báo", f"Thêm khách hàng {makh} thành công!")
        except pyodbc.IntegrityError:
            messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Thêm khách hàng thất bại:\n{e}")

        # --- Thêm thông tin bảng đặt phòng ---
        cursor.execute('''INSERT INTO DatPhong (MaPhong, MaKH, TenKH, NgayDat, NgayNhan, NgayTra)
                                        VALUES (?, ?, ?, ?, ?, ?)''',
                                                (maphong, makh, tenkh, ngaydat, ngaynhan, ngaytra))
        conn.commit()
        # --- Lấy MaDatPhong vừa tạo ---
        cursor.execute("SELECT SCOPE_IDENTITY()")
        madp = cursor.fetchone()[0]

        # Hiển thị vào entry_madp
        self.entry_madp.config(state="normal")
        self.entry_madp.delete(0, tk.END)
        self.entry_madp.insert(0, str(madp))
        self.entry_madp.config(state="disabled")

        # --- Cập nhật bảng phòng ---
        cursor.execute('''UPDATE Phong 
                          SET TrangThai = 'Đã đặt trước'
                          WHERE MaPhong = ?''', (maphong,))
        conn.commit()
        conn.close()
        self.Load_Database_Phong()
        self.Load_Database_DatPhong()
        messagebox.showinfo("Thông báo", "Đặt phòng thành công")
        self.btnDat.config(state = "disabled")

    # ============================= Đặt dịch vụ =============================
    def Datdv_Click(self):
        selected_dp = self.datphong.selection()
        if not selected_dp:
            messagebox.showwarning("Thông báo", "Chưa chọn đặt phòng để đặt dịch vụ!")
            return

        makh = self.entry_makh.get().strip()
        tenkh = self.entry_tenkh.get().strip()
        if not makh or not tenkh:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin khách hàng!")
            return
        madp = self.entry_madp.get().strip()

        if not madp:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn mã đặt phòng!")
            return
        form_ddv = DatDichVu(self, madp)

    # ============================= Nhận phòng =============================
    def Nhanphong_Click(self):
        # Chọn phòng muốn nhận
        selected_datphong = self.datphong.selection()
        if not selected_datphong:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần nhận!")
            return
        item = self.datphong.item(selected_datphong[0])["values"]
        maphong = item[1]
        makh = item[2]

        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''UPDATE Phong 
                          SET TrangThai = 'Đang thuê'
                          WHERE MaPhong = ?''', (maphong,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", f"Khách hàng {makh} đã nhận phòng {maphong}")
        self.Load_Database_Phong()
        self.Load_Database_DatPhong()
        

    # ============================= Hủy =============================
    def Huy_Click(self):
        self.ClearInput()   
        self.entry_madp.config(state="readonly")
        self.entry_maphong.config(state="readonly")
        self.entry_makh.config(state="readonly")
        self.entry_tenkh.config(state="readonly")
        self.entry_cccd.config(state="readonly")
        self.entry_sdt.config(state="readonly")
        self.entry_quoctich.config(state="readonly")

        self.btnHuy.config(state = "disabled")

    # ============================= THOÁT =============================
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiển thị lại form cha
            self.destroy()

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):
        # --- Tiêu đề ---
        self.title_label = tk.Label(self, text="ĐẶT PHÒNG", 
                                    font=("Arial", 20, "bold"), 
                                    fg="#FFAA78", bg="Black")
        self.title_label.place(x=450, y=5, anchor="n", width=700, height=40)

        # --- Frame Thông tin Đặt phòng ---
        self.group = tk.LabelFrame(self, text="Thông tin đặt phòng", font=("Arial", 10),
                                   bg="#000000", fg="#0DFF00")
        self.group.place(relx=0.005, rely=0.23, anchor="w", width=880, height=170)

        # --- Các Entry và Label ---
        tk.Label(self.group, text="Mã đặt phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_madp = tk.Entry(self.group, state="readonly", font=("Arial", 10))        
        self.entry_madp.place(x=120, y=5, width=160, height=20)

        tk.Label(self.group, text="Mã phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_maphong = tk.Entry(self.group, font=("Arial", 10), state = "readonly")        
        self.entry_maphong.place(x=120, y=35, width=160, height=20)

        tk.Label(self.group, text="Mã khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_makh = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_makh.place(x=120, y=65, width=160, height=20)

        tk.Label(self.group, text="Tên khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=95)
        self.entry_tenkh = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_tenkh.place(x=120, y=95, width=160, height=20)

        tk.Label(self.group, text="CCCD", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=125)
        self.entry_cccd = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_cccd.place(x=120, y=125, width=160, height=20)

        # --- Giới tính ---
        tk.Label(self.group, text="Giới tính", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=5)
        self.selected_option = tk.StringVar()
        tk.Radiobutton(self.group, text="Nam", variable=self.selected_option, value="Nam",
                       font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=380, y=5)
        tk.Radiobutton(self.group, text="Nữ", variable=self.selected_option, value="Nữ",
                       font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=450, y=5)

        # --- SĐT và Quốc tịch ---
        tk.Label(self.group, text="SĐT", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=35)
        self.entry_sdt = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_sdt.place(x=380, y=35, width=160, height=20)

        tk.Label(self.group, text="Quốc tịch", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=65)
        self.entry_quoctich = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_quoctich.place(x=380, y=65, width=160, height=20)

        # --- Ngày ---
        tk.Label(self.group, text="Ngày đặt", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=570, y=5)
        self.ngaydat = DateEntry(self.group, date_pattern="dd/mm/yyyy")
        self.ngaydat.place(x=640, y=5, width=160, height=20)

        tk.Label(self.group, text="Ngày nhận", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=570, y=35)
        self.ngaynhan = DateEntry(self.group, date_pattern="dd/mm/yyyy")
        self.ngaynhan.place(x=640, y=35, width=160, height=20)

        tk.Label(self.group, text="Ngày trả", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=570, y=65)
        self.ngaytra = DateEntry(self.group, date_pattern="dd/mm/yyyy")
        self.ngaytra.place(x=640, y=65, width=160, height=20)

        # ============================= Treeview Phòng =============================
        self.frame_phong = tk.Frame(self, bg="black")
        self.frame_phong.place(x=5, y=230, width=550, height=150)

        self.phong = ttk.Treeview(
            self.frame_phong,
            columns=("MaPhong", "LoaiPhong", "TrangThai", "GiaTien"),
            show="headings"
        )

        scroll_y = tk.Scrollbar(self.frame_phong, orient="vertical", command=self.phong.yview)
        self.phong.configure(yscrollcommand=scroll_y.set)
        scroll_x = tk.Scrollbar(self.frame_phong, orient="horizontal", command=self.phong.xview)
        self.phong.configure(xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.phong.pack(fill="both", expand=True)

        self.phong.heading("MaPhong", text="Mã phòng")
        self.phong.heading("LoaiPhong", text="Loại phòng")
        self.phong.heading("TrangThai", text="Trạng thái")
        self.phong.heading("GiaTien", text="Giá tiền")
        self.phong.column("MaPhong", width=80)
        self.phong.column("LoaiPhong", width=150)
        self.phong.column("TrangThai", width=150)
        self.phong.column("GiaTien", width=100)

        # ============================= Treeview Đặt phòng =============================
        self.frame_datphong = tk.Frame(self, bg="black")
        self.frame_datphong.place(x=5, y=390, width=880, height=200)

        self.datphong = ttk.Treeview(
            self.frame_datphong,
            columns=("MaDatPhong", "MaPhong", "MaKH", "TenKH", "NgayDat", "NgayNhan", "NgayTra"),
            show="headings"
        )

        scroll_y2 = tk.Scrollbar(self.frame_datphong, orient="vertical", command=self.datphong.yview)
        self.datphong.configure(yscrollcommand=scroll_y2.set)
        scroll_x2 = tk.Scrollbar(self.frame_datphong, orient="horizontal", command=self.datphong.xview)
        self.datphong.configure(xscrollcommand=scroll_x2.set)
        scroll_y2.pack(side="right", fill="y")
        scroll_x2.pack(side="bottom", fill="x")
        self.datphong.pack(fill="both", expand=True)

        # Chọn dòng
        self.phong.bind("<<TreeviewSelect>>", self.Chon_Dong_Phong)
        self.datphong.bind("<<TreeviewSelect>>", self.Chon_Dong_DatPhong)

        self.datphong.heading("MaDatPhong", text="Mã đặt phòng")
        self.datphong.heading("MaPhong", text="Mã phòng")
        self.datphong.heading("MaKH", text="Mã khách hàng")
        self.datphong.heading("TenKH", text="Tên khách hàng")
        self.datphong.heading("NgayDat", text="Ngày đặt")
        self.datphong.heading("NgayNhan", text="Ngày nhận")
        self.datphong.heading("NgayTra", text="Ngày trả")
        
        self.datphong.column("MaDatPhong", width=100)
        self.datphong.column("MaPhong", width=100)
        self.datphong.column("MaKH", width=100)
        self.datphong.column("TenKH", width=150)
        self.datphong.column("NgayDat", width=120)
        self.datphong.column("NgayNhan", width=120)
        self.datphong.column("NgayTra", width=120)

        # ============================= Buttons =============================
        self.btnNhap = tk.Button(self, text="Nhập thông tin", font=("Arial", 12),
                                 fg="white", bg="#001f4d", command = self.NhapThongTin_Click)
        self.btnNhap.place(x=565, y=230, width=120, height=30)

        self.btnDat = tk.Button(self, text="Đặt", font=("Arial", 12), state = "disabled",
                                 fg="white", bg="#001f4d", command = self.Dat_Click)
        self.btnDat.place(x=695, y=230, width=80, height=30)

        self.btnDatdv = tk.Button(self, text="Đặt dịch vụ", font=("Arial", 12),
                                 fg="white", bg="#ffbb00", command = self.Datdv_Click)
        self.btnDatdv.place(x=565, y=270, width=120, height=30)

        self.btnHuy = tk.Button(self, text="Hủy", font=("Arial", 12), state = "disabled",
                                 fg="white", bg="#001f4d", command = self.Huy_Click)
        self.btnHuy.place(x=695, y=270, width=80, height=30)

        self.btnNhanphong = tk.Button(self, text="Nhận phòng", font=("Arial", 12),
                                 fg="white", bg="#00d0ff", command = self.Nhanphong_Click)
        self.btnNhanphong.place(x=785, y=270, width=100, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                                  fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=785, y=230, width=100, height=30)