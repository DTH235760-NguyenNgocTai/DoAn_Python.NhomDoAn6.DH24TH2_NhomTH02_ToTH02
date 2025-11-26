import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import datetime
from Form_Thanh_Toan import ThanhToan

class TraPhong(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("TRẢ PHÒNG")

        # =================== Thiết lập kích thước và vị trí ===================
        self.window_width = 900
        self.window_height = 600
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

    # =================== Kết nối Database ===================
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

    # =================== Load dữ liệu Phòng ===================
    def Load_Database_Phong(self):
        conn = self.connect_database()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute('''SELECT MaPhong, LoaiPhong, TrangThai, GiaTien 
                          FROM Phong
                          WHERE TrangThai = ?''',("Trống",))   # Chỉ lấy những phòng còn trống
        rows = cursor.fetchall()
        for i in self.phong.get_children():
            self.phong.delete(i)
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.phong.insert("", tk.END, values = clean_row)
        conn.close() 
    
    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

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

        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.datphong.insert("", tk.END, values = clean_row)

        conn.close()

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    def ClearInput(self):
        # --- Xóa và khóa Entry Mã đặt phòng ---
        self.entry_madp.config(state="normal")
        self.entry_madp.delete(0, tk.END)
        self.entry_madp.config(state="disabled")

        # --- Mở các Entry khác để xóa dữ liệu ---
        self.entry_maphong.config(state="normal")
        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")

        # --- Xóa dữ liệu ---
        self.entry_maphong.delete(0, tk.END)
        self.entry_makh.delete(0, tk.END)
        self.entry_tenkh.delete(0, tk.END)

        # --- Reset ngày về ngày hiện tại ---
        self.ngaydat.set_date(datetime.date.today())
        self.ngaynhan.set_date(datetime.date.today())
        self.ngaytra.set_date(datetime.date.today())

        self.btnTraphong.config(state="disabled")
        self.btnHuy.config(state="disabled")

    def Chon_Dong_DatPhong(self, event):
        # Lấy dòng đang được chọn
        selected = self.datphong.selection()
        if selected:
            item = self.datphong.item(selected[0])["values"]

            # item chứa: MaDatPhong, MaPhong, MaKH, TenKH, NgayDat, NgayNhan, NgayTra
            # --- Điền dữ liệu vào các Entry ---
            self.entry_madp.config(state="normal")
            self.entry_madp.delete(0, tk.END)
            self.entry_madp.insert(0, item[0])
            self.entry_madp.config(state="disabled")  # giữ khóa

            self.entry_maphong.config(state="normal")
            self.entry_maphong.delete(0, tk.END)
            self.entry_maphong.insert(0, item[1])
            self.entry_maphong.config(state="readonly")  # chỉ đọc

            self.entry_makh.config(state="normal")
            self.entry_makh.delete(0, tk.END)
            self.entry_makh.insert(0, item[2])
            self.entry_makh.config(state="readonly")

            self.entry_tenkh.config(state="normal")
            self.entry_tenkh.delete(0, tk.END)
            self.entry_tenkh.insert(0, item[3])
            self.entry_tenkh.config(state="readonly")

            # --- Điền ngày đặt, nhận, trả ---
            self.ngaydat.set_date(item[4])
            self.ngaynhan.set_date(item[5])
            self.ngaytra.set_date(item[6])
    
    # ============================= Nhập thông tin ============================= 
    def NhapThongTin_Click(self):
        self.ClearInput()
        # Chọn dòng ở bảng đặt phòng
        selected_datphong = self.datphong.selection()
        if not selected_datphong:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần trả!")
            return    
        
        # Tắt readonly để lấy dữ liệu từ bảng đặt phòng
        self.entry_madp.config(state="normal")
        self.entry_maphong.config(state="normal")
        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")

        item = self.datphong.item(selected_datphong[0])["values"]
        self.entry_madp.insert(0, item[0])
        self.entry_maphong.insert(0, item[1])
        self.entry_makh.insert(0, item[2])
        self.entry_tenkh.insert(0, item[3])

        # Nếu item[4/5/6] là chuỗi 'YYYY-MM-DD' hoặc 'DD/MM/YYYY'
        try:
            # Chuyển đổi ngày nếu là chuỗi
            if isinstance(item[4], str):
                ngaydat_dt = datetime.datetime.strptime(item[4], "%Y-%m-%d").date()
            else:
                ngaydat_dt = item[4]

            if isinstance(item[5], str):
                ngaynhan_dt = datetime.datetime.strptime(item[5], "%Y-%m-%d").date()
            else:
                ngaynhan_dt = item[5]

            if isinstance(item[6], str):
                ngaytra_dt = datetime.datetime.strptime(item[6], "%Y-%m-%d").date()
            else:
                ngaytra_dt = item[6]

            # Gán vào DateEntry
            self.ngaydat.set_date(ngaydat_dt)
            self.ngaynhan.set_date(ngaynhan_dt)
            self.ngaytra.set_date(ngaytra_dt)

        except Exception as e:
            # Nếu lỗi thì đặt ngày hôm nay
            self.ngaydat.set_date(datetime.date.today())
            self.ngaynhan.set_date(datetime.date.today())
            self.ngaytra.set_date(datetime.date.today())

        self.btnTraphong.config(state = "normal")
        self.btnHuy.config(state = "normal")

    # ============================= Trả phòng ============================= 
    def Traphong_Click(self):
        selected_datphong = self.datphong.selection()
        if not selected_datphong:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần trả!")
            return 
        
        madp = self.entry_madp.get().strip()
        result = messagebox.askyesno("Xác nhận", "Bạn có muốn trả phòng")
        if not result:
            return
        tt_window = ThanhToan(self, madp)
        tt_window.grab_set()            # ko cho tương tác vs form trả phòng đến khi đóng form thanh toán
        self.wait_window(tt_window)
        self.Load_Database_Phong()
        self.Load_Database_DatPhong()

    # ============================= HỦY =============================
    def Huy_Click(self):
        self.entry_madp.config(state = "normal")
        self.entry_maphong.config(state = "normal")
        self.entry_makh.config(state = "normal")
        self.entry_tenkh.config(state = "normal")
        self.ngaynhan.set_date(datetime.date.today())
        self.ngaytra.set_date(datetime.date.today())

        self.entry_madp.delete(0, tk.END)
        self.entry_maphong.delete(0, tk.END)
        self.entry_makh.delete(0, tk.END)
        self.entry_tenkh.delete(0, tk.END)

    # ============================= THOÁT =============================
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiển thị lại form cha
            self.destroy()

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):
        # ----------------- Tiêu đề -----------------
        tk.Label(self, text="TRẢ PHÒNG",
                 font=("Arial", 20, "bold"),
                 fg="#FFAA78", bg="black").place(x=450, y=5, anchor="n", width=700, height=40)

        # ----------------- Frame Thông tin Trả phòng -----------------
        group = tk.LabelFrame(self, text="Thông tin trả phòng", font=("Arial", 10),
                              bg="#000000", fg="#0DFF00")
        group.place(relx=0.005, rely=0.23, anchor="w", width=570, height=170)

        # --- Entry Mã đặt phòng ---
        tk.Label(group, text="Mã đặt phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_madp = tk.Entry(group, state="disabled", font=("Arial", 10))
        self.entry_madp.place(x=120, y=5, width=160, height=20)

        # --- Entry Mã phòng ---
        tk.Label(group, text="Mã phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_maphong = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_maphong.place(x=120, y=35, width=160, height=20)

        # --- Entry Mã khách hàng ---
        tk.Label(group, text="Mã khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_makh = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_makh.place(x=120, y=65, width=160, height=20)

        # --- Entry Tên khách hàng ---
        tk.Label(group, text="Tên khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=95)
        self.entry_tenkh = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_tenkh.place(x=120, y=95, width=160, height=20)

        # --- DateEntry Ngày đặt, nhận, trả ---
        tk.Label(group, text="Ngày đặt", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=5)
        self.ngaydat = DateEntry(group, date_pattern="dd/mm/yyyy")
        self.ngaydat.place(x=380, y=5, width=160, height=20)

        tk.Label(group, text="Ngày nhận", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=35)
        self.ngaynhan = DateEntry(group, date_pattern="dd/mm/yyyy")
        self.ngaynhan.place(x=380, y=35, width=160, height=20)

        tk.Label(group, text="Ngày trả", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=65)
        self.ngaytra = DateEntry(group, date_pattern="dd/mm/yyyy")
        self.ngaytra.place(x=380, y=65, width=160, height=20)

        # ----------------- Treeview Phòng -----------------
        frame_phong = tk.Frame(self, bg="black")
        frame_phong.place(x=5, y=230, width=880, height=150)
        self.phong = ttk.Treeview(frame_phong,
                                  columns=("MaPhong", "LoaiPhong", "TrangThai", "GiaTien"),
                                  show="headings")
        scroll_y = tk.Scrollbar(frame_phong, orient="vertical", command=self.phong.yview)
        scroll_x = tk.Scrollbar(frame_phong, orient="horizontal", command=self.phong.xview)
        self.phong.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
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

        # ----------------- Treeview Đặt phòng -----------------
        frame_datphong = tk.Frame(self, bg="black")
        frame_datphong.place(x=5, y=390, width=880, height=200)
        self.datphong = ttk.Treeview(frame_datphong,
                                     columns=("MaDatPhong", "MaPhong", "MaKH", "TenKH", "NgayDat", "NgayNhan", "NgayTra"),
                                     show="headings")
        scroll_y2 = tk.Scrollbar(frame_datphong, orient="vertical", command=self.datphong.yview)
        scroll_x2 = tk.Scrollbar(frame_datphong, orient="horizontal", command=self.datphong.xview)
        self.datphong.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)
        scroll_y2.pack(side="right", fill="y")
        scroll_x2.pack(side="bottom", fill="x")
        self.datphong.pack(fill="both", expand=True)
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

        # ----------------- Buttons -----------------
        self.btnNhap = tk.Button(self, text="Nhập thông tin", font=("Arial", 12), fg="white", bg="#001f4d", command = self.NhapThongTin_Click)
        self.btnNhap.place(x=580, y=62, width=150, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Huy_Click)
        self.btnHuy.place(x=740, y=62, width=150, height=30)

        self.btnTraphong = tk.Button(self, text="Trả phòng", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Traphong_Click)
        self.btnTraphong.place(x=580, y=110, width=150, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=740, y=110, width=150, height=30)