import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Dang_Nhap import DangNhap  
from Form_Dat_Phong import DatPhong
from Form_Tra_Phong import TraPhong

class TrangChu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TRANG CHỦ")
        self.geometry("900x600")
        self.center_window(900, 600)

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()

    def center_window(self, w, h):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        
    # Hàm đóng form
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

    def DatPhong_Click(self):
        DatPhong(self).grab_set()

    def TraPhong_Click(self):
        TraPhong(self).grab_set()

    def Sign_in_Click(self):  # Ẩn TrangChu khi mở login
        login = DangNhap(self)
        login.grab_set()

    def TaoGiaoDien(self):
        # Background
        hinhnen = Image.open(r"E:\Hình ảnh khách sạn_DotNet\Ảnh-trang-chủ.png")
        size_nen = hinhnen.resize((900, 600))
        hinhnen_photo = ImageTk.PhotoImage(size_nen)
        self.bg_label = tk.Label(self, image=hinhnen_photo)
        self.bg_label.image = hinhnen_photo
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Top frame
        top_frame = tk.Frame(self, bg="#000000")
        top_frame.place(x=0, y=0, width=900, height=35)

        # Sign in button
        btn_sign = tk.Button(top_frame, text="Sign in", bg="#2600FF", fg="white",
                             font=("Arial", 12, "bold"), command=self.Sign_in_Click)
        btn_sign.place(x=100, rely=0.5, anchor="center", width=100, height=30)

        # Nút Đặt phòng
        btndatphong = tk.Button(top_frame, text="Đặt phòng", bg="#2600FF", fg="white",
                                font=("Arial", 12, "bold"), command=self.DatPhong_Click)
        btndatphong.place(relx=0.5, rely=0.5, anchor="e")

        # Nút Trả phòng
        btntraphong = tk.Button(top_frame, text="Trả phòng", bg="#246A03", fg="white",
                                font=("Arial", 12, "bold"), command=self.TraPhong_Click)
        btntraphong.place(relx=0.5, rely=0.5, anchor="w")

        # Tên khách sạn
        tk.Label(self, text="ONE THOUSAND AND ONE NIGHTS HOTEL", font=("Segoe Script", 20, "italic"),
                 fg="yellow", bg="#000000").place(relx=0.5, y=60, anchor="n", width=700, height=40)

if __name__ == "__main__":
    app = TrangChu()
    app.mainloop()
