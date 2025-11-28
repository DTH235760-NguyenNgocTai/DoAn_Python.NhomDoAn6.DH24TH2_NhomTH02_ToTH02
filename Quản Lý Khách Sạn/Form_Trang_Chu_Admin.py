import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from QL_Phong import Room_Manage
from QL_Nhan_Su import Staff_Manage
from QL_Dich_Vu import Service_Manage
from QL_Khach_Hang import Customer_Manage
from QL_Chi_Tiet_Dich_Vu import ServiceDetail_Manage
from Form_UpdateUser import CapNhatNhanSu

class FormTrangChuAdmin(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent    #Trang chủ
        self.title("TRANG CHỦ _ ADMIN")
        self.window_width = 900
        self.window_height = 600

        self.transient(parent)
        self.grab_set()
        
        self.center_window(self.window_width, self.window_height)
        self.resizable(False, False)

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()

    # ============================= Các hàm liên kết form =============================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()  # hiện lại TrangChu
            self.destroy()

    # ============================= HÀM ĐƯA ADMIN LÊN LẠI =============================
    def return_from_child(self, child_window):
        child_window.destroy()
        self.deiconify()  # Hiện lại form Admin
        self.lift()       # Đưa form Admin lên trên
        self.focus_force()
    
    # ============================= HÀM MỞ FORM CON =============================
    def open_child_form(self, FormClass):
        """Hàm mở form con chuẩn hóa."""
        child = FormClass(self)

        # Khi đóng child → tự động trả về Admin
        child.protocol("WM_DELETE_WINDOW", lambda: self.return_from_child(child))

        child.grab_set()   # Khóa focus vào form con
        child.lift()
            
    def Phong_Click(self):
        self.open_child_form(Room_Manage)

    def NhanSu_Click(self):
        self.open_child_form(Staff_Manage)

    def DichVu_Click(self):
        self.open_child_form(Service_Manage)

    def CTDV_Click(self):
        self.open_child_form(ServiceDetail_Manage)

    def KhachHang_Click(self):
        self.open_child_form(Customer_Manage)

    def CapNhatNhanSu_Click(self):
        self.open_child_form(CapNhatNhanSu)

    # ============================= ĐĂNG XUẤT =============================
    def Sign_out_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()
            self.destroy()

    def center_window(self, w, h):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        
    def TaoGiaoDien(self):
        # ============================= Background =============================
        hinhnen = Image.open("E:\Hình ảnh khách sạn_DotNet\Ảnh-trang-chủ.png")
        size_nen = hinhnen.resize((900, 600))
        hinhnen_photo = ImageTk.PhotoImage(size_nen)
        self.bg_label = tk.Label(self, image=hinhnen_photo)
        self.bg_label.image = hinhnen_photo
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ============================= Top Frame =============================
        top_frame = tk.Frame(self, bg="#000000")  # Header
        top_frame.place(x=0, y=0, width=900, height=30)

        # Icon user
        icon_user = Image.open("E:\Hình ảnh khách sạn_DotNet\Icon Sign in.png")
        size_icon = icon_user.resize((50, 30))
        icon_photo = ImageTk.PhotoImage(size_icon)
        user_icon = tk.Label(top_frame, image=icon_photo, bg="#000000")
        user_icon.image = icon_photo
        user_icon.place(x=20, rely=0.5, anchor="center", width=40, height=40)

        # Nút Sign out
        btn_signout = tk.Button(top_frame, text="Sign out", bg="#FF0000", fg="white",
                                font=("Arial", 12, "bold"), command=self.Sign_out_Click)
        btn_signout.place(x=850, rely=0.5, anchor="center", width=100, height=30)

        # Các nút chức năng
        # ============================= Các nút chức năng trong top frame =============================
        button_width = 110
        start_x = 120   # vị trí nút đầu tiên (sau icon user)
        spacing = 115   # khoảng cách nút đều nhau

        btn_phong = tk.Button(top_frame, text="Phòng", bg="#246A03", fg="white",
                          font=("Arial", 12, "bold"), command=self.Phong_Click)
        btn_phong.place(x=start_x, rely=0.5, anchor="center", width=button_width, height=30)

        btn_nhansu = tk.Button(top_frame, text="Nhân sự", bg="#246A03", fg="white",
                           font=("Arial", 12, "bold"), command=self.NhanSu_Click)
        btn_nhansu.place(x=start_x + spacing, rely=0.5, anchor="center", width=button_width, height=30)

        btn_dichvu = tk.Button(top_frame, text="Dịch vụ", bg="#246A03", fg="white",
                           font=("Arial", 12, "bold"), command=self.DichVu_Click)
        btn_dichvu.place(x=start_x + spacing * 2, rely=0.5, anchor="center", width=button_width, height=30)

        btn_ctdv = tk.Button(top_frame, text="CTDV", bg="#246A03", fg="white",
                         font=("Arial", 12, "bold"), command=self.CTDV_Click)
        btn_ctdv.place(x=start_x + spacing * 3, rely=0.5, anchor="center", width=button_width, height=30)

        btn_khachhang = tk.Button(top_frame, text="Khách hàng", bg="#246A03", fg="white",
                              font=("Arial", 12, "bold"), command=self.KhachHang_Click)
        btn_khachhang.place(x=start_x + spacing * 4, rely=0.5, anchor="center", width=button_width, height=30)

        btn_update_user = tk.Button(top_frame, text="Update User", bg="#246A03", fg="white",
                                font=("Arial", 12, "bold"), command=self.CapNhatNhanSu_Click)
        btn_update_user.place(x=start_x + spacing * 5, rely=0.5, anchor="center", width=button_width, height=30)


        # Tên khách sạn
        tk.Label(self, text="ONE THOUSAND AND ONE NIGHTS HOTEL",
                 font=("Segoe Script", 20, "italic"),
                 fg="yellow", bg="#001f4d").place(relx=0.5, y=60, anchor="n", width=700, height=40)