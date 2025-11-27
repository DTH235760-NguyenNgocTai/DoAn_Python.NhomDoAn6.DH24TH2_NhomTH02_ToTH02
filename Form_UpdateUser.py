import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
import pyodbc           # Kết nối Database
from PIL import Image, ImageTk

class CapNhatNhanSu(tk.Toplevel):     
    def __init__(self, parent=None):
        super().__init__(parent)     # Gọi constructor của Toplevel
        self.parent = parent
        self.thaotac = 0
        self.title("CẬP NHẬT NHÂN SỰ")  

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
        self.Load_Database_NhanSu()
        self.Load_Database_DangNhap()

    # ============================= Kết nối CSDL =============================
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
        
    # ============================= Load dữ liệu nhân sự =============================
    def Load_Database_NhanSu(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaNV, TenNV, NgaySinh, GioiTinh, SoDienThoai, ChucVu
                          FROM NhanVien
                          WHERE ChucVu = ? Or ChucVu = ?''', ("Quản lý", "Giám đốc"))
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.nhansu.get_children():
            self.nhansu.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]    # Xóa các kí tự '' và () trước khi đưa vào bảng
            self.nhansu.insert("", tk.END, values = clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()
            
    # ============================= Load dữ liệu đăng nhập =============================
    def Load_Database_DangNhap(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT Username, Password, MaNV
                          FROM DangNhap''')
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.dangnhap.get_children():
            self.dangnhap.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]    # Xóa các kí tự '' và () trước khi đưa vào bảng
            self.dangnhap.insert("", tk.END, values = clean_row)

        conn.close()

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # --- Chọn dòng nhân viên---
    def Chon_Dong_NV(self, event):
        if self.thaotac != 0:
            return  # khi đang Thêm hoặc Sửa → không auto fill

        selected = self.nhansu.selection()
        if selected:
            item = self.nhansu.item(selected[0])["values"]

            self.entry_manv.config(state="normal")
            self.entry_manv.delete(0, tk.END)
            self.entry_manv.insert(0, item[0])
            self.entry_manv.config(state="readonly")

            self.entry_tennv.delete(0, tk.END)
            self.entry_tennv.insert(0, item[1])

    # --- Chọn dòng đăng nhập ---
    def Chon_Dong_DN(self, event):
        if self.thaotac != 0:
            return  # khi đang Thêm hoặc Sửa → không auto fill
        selected = self.dangnhap.selection()
        if selected:
            item = self.dangnhap.item(selected[0])["values"]
            self.entry_username.config(state = "normal")
            self.entry_username.delete(0, tk.END)
            self.entry_username.insert(0, item[0])
            self.entry_username.config(state = "readonly")

            self.entry_password.config(state = "normal")
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, item[1])
            self.entry_password.config(state = "readonly")

            self.entry_manv.config(state="normal")
            self.entry_manv.delete(0, tk.END)
            self.entry_manv.insert(0, item[2])
            self.entry_manv.config(state="readonly")
            
            # Lấy Tên nhân viên trực tiếp từ database
            manv = self.entry_manv.get().strip()
            conn = self.connect_database()
            cursor = conn.cursor()
            cursor.execute("SELECT TenNV FROM NhanVien WHERE MaNV = ?", (manv,))
            result = cursor.fetchone()
            conn.close()

            tennv = result[0]

            # Hiển thị Tên nhân viên
            self.entry_tennv.config(state="normal")
            self.entry_tennv.delete(0, tk.END)
            self.entry_tennv.insert(0, tennv)
            self.entry_tennv.config(state="readonly")

    def ClearInput(self):
        self.entry_username.config(state = "normal")
        self.entry_password.config(state = "normal")
        self.entry_manv.config(state="normal")
        self.entry_tennv.config(state="normal")

        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_manv.delete(0, tk.END)
        self.entry_tennv.delete(0, tk.END)

        self.entry_username.config(state = "readonly")
        self.entry_password.config(state = "readonly")
        self.entry_manv.config(state="readonly")
        self.entry_tennv.config(state="readonly")

    def Check_TrungUser(self, user):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM DangNhap WHERE Username = ?''', (user,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False
    # ============================= Thêm =============================
    def Them_Click(self):
        self.ClearInput()
        self.thaotac = 1
        self.entry_username.focus_set()
        self.btnLuu.config(state = "normal")
        self.btnHuy.config(state = "normal")

    # ============================= Sửa =============================
    def Sua_Click(self):
        selected = self.dangnhap.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn thông tin cần cập nhật!")
            return
        self.thaotac = 2
        self.ClearInput()
        self.entry_username.config(state = "normal")
        self.entry_password.config(state = "normal")

        item = self.dangnhap.item(selected[0])["values"]

        self.entry_username.insert(0, item[0])
        self.entry_password.insert(0, item[1])

        self.btnLuu.config(state = "normal")
        self.btnHuy.config(state = "normal")

    # ============================= Xóa =============================   
    def Xoa_Click(self):
        selected = self.dangnhap.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn thông tin cần cập nhật!")
            return
        item = self.dangnhap.item(selected[0])["values"]
        user = item[0]

        if not messagebox.askyesno("Xác nhận", f"Bạn muốn xóa username {user}?"):
            return
        
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM DangNhap WHERE Username = ?''', (user,))        
        conn.commit()
        conn.close()
        self.Load_Database_DangNhap()

    # ============================= Xóa ============================= 
    def Luu_Click(self):
        user = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        manv = self.entry_manv.get().strip()
        tennv = self.entry_tennv.get().strip()

        if not user or not password or not manv or not tennv:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if self.thaotac == 1:
            if self.Check_TrungUser(user):
                messagebox.showwarning("Thông báo", "Username đã tồn tại trong hệ thống!")
                return
        
        conn = self.connect_database()
        cursor = conn.cursor()

        if self.thaotac == 1:
            try:
                cursor.execute(
                    "INSERT INTO DangNhap VALUES (?, ?, ?)",
                    (user, password, manv)
                )
                conn.commit()
                messagebox.showinfo("Thông báo", f"Thêm user {user} thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        elif self.thaotac == 2:
            cursor.execute(
                "UPDATE DangNhap SET Password = ? WHERE Username = ?",
                (password, user)
            )
            conn.commit()
            messagebox.showinfo("Thông báo", f"Cập nhật user {user} thành công!")
            self.Load_Database_DangNhap()

    # ============================= Xóa ============================= 
    def Huy_Click(self):
        self.ClearInput()
        self.entry_username.config(state="readonly")
        self.entry_password.config(state="readonly")
        self.entry_manv.config(state="readonly")
        self.entry_tennv.config(state="readonly")
        self.btnHuy.config(state="disabled")
        self.btnLuu.config(state="disabled")
        self.thaotac = 0

    # ======================= THOÁT =======================
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy() 

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):
        # Icon user
        icon_user = Image.open("E:\Hình ảnh khách sạn_DotNet\Icon Sign in.png")
        self.size_icon = icon_user.resize((50, 30))
        self.icon_photo = ImageTk.PhotoImage(self.size_icon)

        user_icon = tk.Label(self, image = self.icon_photo, bg = "#000000", fg = "white")
        user_icon.place(x = 25, rely = 0.05, anchor = "center", width = 40, height = 40)

        tk.Label(self, text="ADMIN", fg="salmon", bg="#000000", font=("Arial", 10, "bold")).place(x=10, y=50)

        tk.Label(self, text="CẬP NHẬT NHÂN SỰ", fg="#FF6A00", bg="#000000", font=("Segoe UI", 20, "bold")).place(relx=0.5, y=10, anchor="n")

        # === Group thông tin đăng nhập ===
        self.group = tk.LabelFrame(
            self,                              
            text="Thông tin đăng nhập",
            font=("Arial", 10), fg="#0DFF00", bg="#000000"
        )
        self.group.place(x=10, y=150, anchor="w", width=270, height=150)

        tk.Label(self.group, text = "Username", font=("Arial", 10), fg="#FCBD00", bg="#000000").grid(column = 0, row = 0, sticky = "w")
        self.entry_username = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_username.grid(column = 1, row = 0)

        tk.Label(self.group, text = "Password", font=("Arial", 10), fg="#FCBD00", bg="#000000").grid(column = 0, row = 1, sticky = "w")
        self.entry_password = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_password.grid(column = 1, row = 1)

        tk.Label(self.group, text = "Mã nhân viên", font=("Arial", 10), fg="#FCBD00", bg="#000000").grid(column = 0, row = 2, sticky = "w")
        self.entry_manv = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_manv.grid(column = 1, row = 2)

        tk.Label(self.group, text = "Tên nhân viên", font=("Arial", 10), fg="#FCBD00", bg="#000000").grid(column = 0, row = 3, sticky = "w")
        self.entry_tennv = tk.Entry(self.group, font=("Arial", 10), state = "readonly")
        self.entry_tennv.grid(column = 1, row = 3)

        # === Bảng nhân sự ===
        frame_nhansu = tk.Frame(self, bg="white")
        frame_nhansu.place(x=10, y=250, width=880, height=250)

        self.nhansu = ttk.Treeview(frame_nhansu,
                                   columns=("MaNV", "TenNV", "NgaySinh", "GioiTinh", "SoDienThoai", "ChucVu"),
                                   show="headings")

        # Scrollbar
        scroll_y = tk.Scrollbar(frame_nhansu, orient="vertical", command=self.nhansu.yview)
        self.nhansu.configure(yscrollcommand=scroll_y.set)
        scroll_x = tk.Scrollbar(frame_nhansu, orient="horizontal", command=self.nhansu.xview)
        self.nhansu.configure(xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.nhansu.pack(fill="both", expand=True)

        # Chọn dòng
        self.nhansu.bind("<<TreeviewSelect>>", self.Chon_Dong_NV)

        # Các cột
        self.nhansu.heading("MaNV", text="Mã nhân viên")
        self.nhansu.heading("TenNV", text="Tên nhân viên")
        self.nhansu.heading("NgaySinh", text="Ngày sinh")
        self.nhansu.heading("GioiTinh", text="Giới tính")
        self.nhansu.heading("SoDienThoai", text="Số điện thoại")
        self.nhansu.heading("ChucVu", text="Chức vụ")

        self.nhansu.column("MaNV", width=100)
        self.nhansu.column("TenNV", width=210)
        self.nhansu.column("NgaySinh", width=140)
        self.nhansu.column("GioiTinh", width=70)
        self.nhansu.column("SoDienThoai", width=140)
        self.nhansu.column("ChucVu", width=200)

        # === Bảng đăng nhập ===
        frame_dangnhap = tk.Frame(self, bg="white")
        frame_dangnhap.place(x=300, y=80, width=580, height=150)

        self.dangnhap = ttk.Treeview(frame_dangnhap,
                                   columns=("Username", "Password", "MaNV"),
                                   show="headings")
        self.dangnhap.heading("Username", text="Username")
        self.dangnhap.heading("Password", text="Password")
        self.dangnhap.heading("MaNV", text="Mã nhân viên")
        self.dangnhap.pack(fill="both", expand=True)

        self.dangnhap.bind("<<TreeviewSelect>>", self.Chon_Dong_DN)

        self.dangnhap.column("Username", width=200)
        self.dangnhap.column("Password", width=200)
        self.dangnhap.column("MaNV", width=180)

        # Nút chức năng
        self.btnThem = tk.Button(self, text="Thêm", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Them_Click)
        self.btnThem.place(x=150, y=530, width=90, height=30)

        self.btnXoa = tk.Button(self, text="Xoá", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Xoa_Click)
        self.btnXoa.place(x = 250, y=530, width=90, height=30)

        self.btnSua = tk.Button(self, text="Sửa", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Sua_Click)
        self.btnSua.place(x=350, y=530, width=90, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Huy_Click)
        self.btnHuy.place(x=450, y=530, width=90, height=30)

        self.btnLuu = tk.Button(self, text="Lưu", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled",  command = self.Luu_Click)
        self.btnLuu.place(x=550, y=530, width=90, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=650, y=530, width=90, height=30)