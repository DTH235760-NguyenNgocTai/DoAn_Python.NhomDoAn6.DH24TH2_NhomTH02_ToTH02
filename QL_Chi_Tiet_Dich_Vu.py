import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
import pyodbc           # Kết nối Database

class ServiceDetail_Manage(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("QUẢN LÝ CHI TIẾT DỊCH VỤ")
        # Kích thước form
        window_width = 650
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
        # Chỉnh màu nền của form
        self.configure(bg="#000000")

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        self.Load_Database_CTDV()

    # ============================= Kết nối Cơ Sở Dữ Liệu =============================
    # ----------------------------- Liên kết CSDL -----------------------------
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

    # ----------------------------- Load CSDL -----------------------------
    def Load_Database_CTDV(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaCTDV, MaDatPhong, MaDV, SoLuong 
                          FROM ChiTietDichVu''')
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.ctdv.get_children():
            self.ctdv.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]    # Xóa các kí tự '' và () trước khi đưa vào bảng
            self.ctdv.insert("", tk.END, values=clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

    # ================== CHỌN DÒNG ==================
    def Chon_Dong(self, event):
        # Lấy dòng đang được chọn
        selected = self.ctdv.selection()
        if selected:
            item = self.ctdv.item(selected[0])["values"]

            # Điền dữ liệu vào các entry
            self.entry_mactdv.config(state="normal")
            self.entry_mactdv.delete(0, tk.END)
            self.entry_mactdv.insert(0, item[0])
            self.entry_mactdv.config(state="readonly")

            self.entry_madp.config(state="normal")
            self.entry_madp.delete(0, tk.END)
            self.entry_madp.insert(0, item[1])
            self.entry_madp.config(state="readonly")

            self.entry_madv.config(state="normal")
            self.entry_madv.delete(0, tk.END)
            self.entry_madv.insert(0, item[2])
            self.entry_madv.config(state="readonly")

            self.entry_sl.config(state="normal")
            self.entry_sl.delete(0, tk.END)
            self.entry_sl.insert(0, item[3])
            self.entry_sl.config(state="readonly")

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    def XemChiTiet_Click(self):
        selected = self.ctdv.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn thông tin muốn xem!")
            return
        
        item = self.ctdv.item(selected[0])["values"]
        # Tắt readonly để nhập dữ liệu
        self.entry_mactdv.config(state="normal")
        self.entry_madp.config(state="normal")
        self.entry_maphong.config(state="normal")
        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")
        self.entry_madv.config(state="normal")
        self.entry_tendv.config(state="normal")
        self.entry_sl.config(state="normal")

        # Xóa dữ liệu trong entry
        self.entry_mactdv.delete(0, tk.END)
        self.entry_madp.delete(0, tk.END)
        self.entry_maphong.delete(0, tk.END)
        self.entry_makh.delete(0, tk.END)
        self.entry_tenkh.delete(0, tk.END)
        self.entry_madv.delete(0, tk.END)
        self.entry_tendv.delete(0, tk.END)
        self.entry_sl.delete(0, tk.END)
        conn = self.connect_database()
        cursor = conn.cursor()

        cursor.execute('''SELECT ct.MaCTDV, dp.MaDatPhong, dp.MaPhong, kh.MaKH, kh.TenKH, ct.MaDV, dv.TenDV, ct.SoLuong
                          FROM DatPhong dp
                          JOIN KhachHang kh ON dp.MaKH = kh.MaKH
                          JOIN ChiTietDichVu ct ON dp.MaDatPhong = ct.MaDatPhong
                          JOIN DichVu dv ON ct.MaDV = dv.MaDV
                          WHERE ct.MaCTDV = ?''', (item[0],))
        result = cursor.fetchone()  # Lưu kết quả truy vấn
        conn.close()

        # Nhập dữ liệu vào entry
        self.entry_mactdv.insert(0, result[0])
        self.entry_madp.insert(0, result[1])
        self.entry_maphong.insert(0, result[2])
        self.entry_makh.insert(0, result[3])
        self.entry_tenkh.insert(0, result[4])
        self.entry_madv.insert(0, result[5])
        self.entry_tendv.insert(0, result[6])
        self.entry_sl.insert(0, result[7])

        self.entry_mactdv.config(state="readonly")
        self.entry_madp.config(state="readonly")
        self.entry_maphong.config(state="readonly")
        self.entry_makh.config(state="readonly")
        self.entry_tenkh.config(state="readonly")
        self.entry_madv.config(state="readonly")
        self.entry_tendv.config(state="readonly")
        self.entry_sl.config(state="readonly")

    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiển thị lại form cha
            self.destroy()         

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):
        # ----------------------------- Tên form -----------------------------
        title_label = tk.Label(self, text="QUẢN LÝ CHI TIẾT DỊCH VỤ",
                               font=("Arial", 20, "bold"),
                               fg="#FFAA78",
                               bg="Black")
        title_label.place(relx = 0.5, y=5, anchor="n", width=700, height=40)

        # ----------------------------- Thông tin dịch vụ (Chứa trong Frame) -----------------------------
        group = tk.LabelFrame(self, text="Thông tin dịch vụ", font=("Arial", 10),
                              fg="#0DFF00",
                              bg="#000000")
        group.place(x=10, y=140, anchor="w", width=600, height=180)

        # --- Mã chi tiết dịch vụ ---
        tk.Label(group, text="Mã CTDV", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_mactdv = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_mactdv.place(x=120, y=5, width=160, height=20)

        # --- Mã đặt phòng ---
        tk.Label(group, text="Mã đặt phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_madp = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_madp.place(x=120, y=35, width=160, height=20)

        # --- Mã phòng ---
        tk.Label(group, text="Mã phòng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_maphong = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_maphong.place(x=120, y=65, width=160, height=20)

        # --- Mã khách hàng ---
        tk.Label(group, text="Mã khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=95)
        self.entry_makh = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_makh.place(x=120, y=95, width=160, height=20)

        # --- Tên khách hàng ---
        tk.Label(group, text="Tên khách hàng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=125)
        self.entry_tenkh = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_tenkh.place(x=120, y=125, width=160, height=20)

        # --- Mã dịch vụ ---
        tk.Label(group, text="Mã dịch vụ", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=5)
        self.entry_madv = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_madv.place(x=390, y=5, width=160, height=20)

        # --- Tên dịch vụ ---
        tk.Label(group, text="Tên dịch vụ", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=35)
        self.entry_tendv = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_tendv.place(x=390, y=35, width=160, height=20)

        # --- Số lượng ---
        tk.Label(group, text="Số lượng", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=310, y=65)
        self.entry_sl = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_sl.place(x=390, y=65, width=160, height=20)

        # ----------------------------- Bảng Chi tiết dịch vụ -----------------------------
        frame_ctdv = tk.Frame(self, bg="black")
        frame_ctdv.place(x=10, y=250, width=600, height=150)

        self.ctdv = ttk.Treeview(frame_ctdv,
                            columns=("MaCTDV", "MaDatPhong", "MaDV", "SoLuong"),
                            show="headings")

        # Tạo Scrollbar dọc
        scroll_y = tk.Scrollbar(frame_ctdv, orient="vertical", command = self.ctdv.yview)
        self.ctdv.configure(yscrollcommand=scroll_y.set)

        # Tạo Scrollbar ngang
        scroll_x = tk.Scrollbar(frame_ctdv, orient="horizontal", command = self.ctdv.xview)
        self.ctdv.configure(xscrollcommand=scroll_x.set)

        # Hiển thị Scrollbar
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # Hiển thị Treeview rộng hết cả frame chứa và thay đổi theo kích thước frame
        self.ctdv.pack(fill="both", expand=True)

        # Khai báo các cột
        self.ctdv.heading("MaCTDV", text="Mã CTDV")
        self.ctdv.heading("MaDatPhong", text="Mã đặt phòng")
        self.ctdv.heading("MaDV", text="Mã dịch vụ")
        self.ctdv.heading("SoLuong", text="Số lượng")

        self.ctdv.column("MaCTDV", width=80)
        self.ctdv.column("MaDatPhong", width=150)
        self.ctdv.column("MaDV", width=150)
        self.ctdv.column("SoLuong", width=100)

        # Chọn dòng
        self.ctdv.bind("<<TreeviewSelect>>", self.Chon_Dong)

        # ============================= Chức năng =============================
        # --- Xem chi tiết ---
        btnXemchitiet = tk.Button(self, text="Xem chi tiết", font=("Arial", 12),
                                  fg="white", bg="#001f4d", command = self.XemChiTiet_Click)
        btnXemchitiet.place(x=10, y=420, width=100, height=30)

        # --- Thoát ---
        btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                             fg="white", bg="#001f4d", command = self.Thoat_Click)
        btnThoat.place(x=510, y=420, width=100, height=30)