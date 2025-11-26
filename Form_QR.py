import tkinter as tk
from tkinter import ttk , messagebox    #Dùng combobox, messagebox
from PIL import Image, ImageTk      #Chèn hình ảnh

class QRCode(tk.Toplevel):
    def __init__(self, parent=None, image_path=None):
        super().__init__(parent)
        self.parent = parent
        self.title("QR Code")
        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # =================== Kích thước và vị trí ===================
        self.window_width = 200
        self.window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Load hình QR
        hinhnen = Image.open(r"E:\Hình ảnh khách sạn_DotNet\QR Code.png")
        size_nen = hinhnen.resize((200, 200))
        self.hinhnen_photo = ImageTk.PhotoImage(size_nen)

        bg_label = tk.Label(self, image=self.hinhnen_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()