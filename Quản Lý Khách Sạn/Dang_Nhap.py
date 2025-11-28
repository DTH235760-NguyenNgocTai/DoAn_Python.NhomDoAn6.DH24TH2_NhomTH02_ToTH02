import tkinter as tk
from tkinter import messagebox
import pyodbc
from Form_Trang_Chu_Admin import FormTrangChuAdmin

class DangNhap(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent    # Trang chủ
        self.title("Đăng nhập")
        self.window_width = 400
        self.window_height = 200

        self.transient(parent)
        self.grab_set()

        # Căn giữa màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()

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

    # ============================= Sự kiện =============================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiện lại TrangChu
                self.parent.lift()         # đưa TrangChu lên trên
                self.parent.focus_force()  # focus vào TrangChu
            self.destroy()
    
    def return_to_home(self, admin_window):
        admin_window.destroy()
        if self.parent:
            self.parent.deiconify()
        self.destroy()
            
    def DangNhap_Click(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username:
            messagebox.showwarning("Thông báo", "Vui lòng nhập Username!")
            return
        if not password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập Password!")
            return

        conn = self.connect_database()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM DangNhap WHERE Username=? AND Password=?", (username, password))
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            self.withdraw()  # Ẩn form login
            admin_window = FormTrangChuAdmin(self.parent)  # parent là TrangChu
            admin_window.grab_set()
            admin_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_home(admin_window))

        else:
            messagebox.showerror("Lỗi", "Đăng nhập thất bại! Vui lòng kiểm tra lại tài khoản và mật khẩu.")
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus_set()

    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

    # ============================= Giao diện =============================
    def TaoGiaoDien(self):
        tk.Label(self, text="Username:", font=("Arial", 12)).place(x=30, y=30)
        self.entry_username = tk.Entry(self, font=("Arial", 12))
        self.entry_username.place(x=130, y=30, width=200)

        tk.Label(self, text="Password:", font=("Arial", 12)).place(x=30, y=70)
        self.entry_password = tk.Entry(self, font=("Arial", 12), show="*")
        self.entry_password.place(x=130, y=70, width=200)

        self.btn_login = tk.Button(self, text="Đăng nhập", font=("Arial", 12), bg="#001f4d", fg="white",
                                   command=self.DangNhap_Click)
        self.btn_login.place(x=130, y=120, width=100, height=30)

        self.btn_thoat = tk.Button(self, text="Thoát", font=("Arial", 12), bg="#001f4d", fg="white",
                                   command=self.Thoat_Click)
        self.btn_thoat.place(x=240, y=120, width=100, height=30)