import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc

class DatDichVu(tk.Toplevel):
    def __init__(self, parent=None, madp=None):
        super().__init__(parent)
        self.parent = parent
        self.madp = madp # Lưu giá trị mã đặt phòng truyền từ form đặt phòng

        self.transient(parent)
        self.grab_set()

        self.title("ĐẶT DỊCH VỤ")
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
        self.Load_Database_DichVu()
        self.Load_Database_CTDV()
        # Gán mã đặt phòng vào entry
        if self.madp:
            self.entry_madp.config(state="normal")
            self.entry_madp.insert(0, self.madp)
            self.entry_madp.config(state="disabled")

    # ======================= KẾT NỐI CSDL =======================
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

    # ======================= LOAD DATABASE =======================
    def Load_Database_DichVu(self):
        conn = self.connect_database()
        if conn is None: return
        cursor = conn.cursor()
        cursor.execute('SELECT MaDV, TenDV, GiaDV FROM DichVu')
        rows = cursor.fetchall()
        for i in self.dichvu.get_children():
            self.dichvu.delete(i)
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.dichvu.insert("", tk.END, values = clean_row)
        conn.close()

    def Load_Database_CTDV(self):
        conn = self.connect_database()
        if conn is None: return
        cursor = conn.cursor()
        cursor.execute('SELECT MaCTDV, MaDatPhong, MaDV, SoLuong FROM ChiTietDichVu')
        rows = cursor.fetchall()
        for i in self.ctdv.get_children():
            self.ctdv.delete(i)
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.ctdv.insert("", tk.END, values = clean_row)
        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()  # hiện lại form cha
            self.destroy()
            
    # ================== CHỌN DÒNG DỊCH VỤ ==================
    def Chon_Dong_DichVu(self, event):
        # Lấy dòng đang được chọn
        selected = self.dichvu.selection()
        if selected:
            item = self.dichvu.item(selected[0])["values"]

            self.entry_madv.config(state="normal")
            self.entry_madv.delete(0, tk.END)
            self.entry_madv.insert(0, item[0])  # Lấy mã dịch vụ
            self.entry_madv.config(state="readonly")

    # --- Check số lượng ---
    def Check_Soluong(self, sl):
        if sl.isdigit():
            return True
        else:
            return False

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================        
    # ============================= ClearInput =============================
    def ClearInput(self):
        # Xóa entry trừ mã đặt phòng
        self.entry_maddv.config(state="normal")
        self.entry_maddv.delete(0, tk.END)
        self.entry_maddv.config(state="disabled")
    
        self.entry_madv.config(state="normal")
        self.entry_madv.delete(0, tk.END)
        self.entry_madv.config(state="readonly")
    
        self.entry_sl.delete(0, tk.END)

        # Giữ mã đặt phòng, chỉ xóa khi không có madp
        if not self.madp:
            self.entry_madp.config(state="normal")
            self.entry_madp.delete(0, tk.END)
            self.entry_madp.config(state="disabled")

    # ============================= Nhập thông tin =============================
    def NhapThongTin_Click(self):
        selected = self.dichvu.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn dịch vụ!")
            return
        item = self.dichvu.item(selected[0])["values"]
        self.entry_madv.config(state="normal")
        self.entry_madv.delete(0, tk.END)
        self.entry_madv.insert(0, item[0])
        self.entry_madv.config(state="readonly")
        self.entry_sl.focus_set()
        self.btnDat.config(state="normal")
        self.btnHuy.config(state="normal")

    # ============================= Nhập thông tin =============================
    def Dat_Click(self):
        madv = self.entry_madv.get().strip()
        soluong = self.entry_sl.get().strip()
        if not madv:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn dịch vụ cần đặt!")
            return  

        if not soluong:
            messagebox.showwarning("Thông báo", "Bạn chưa nhập số lượng cần đặt!")
            return
        
        if not self.Check_Soluong(soluong):
            messagebox.showwarning("Thông báo", "Số lượng phải là số!")
            return
        
        result = messagebox.askyesno("Xác nhận", f"Bạn có muốn đặt dịch vụ {madv} không?")
        if not result:
            return        
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO ChiTietDichVu (MaDatPhong, MaDV, SoLuong)
                                             VALUES (?, ?, ?)''',
                                                    (self.madp, madv, int(soluong)))
        conn.commit()
        conn.close()
        self.Load_Database_CTDV()
        messagebox.showinfo("Thông báo", f"Đã đặt dịch vụ {madv} thành công")
        self.btnDat.config(state = "disabled")
        self.btnHuy.config(state = "disabled") 

    # ============================= Hủy =============================
    def Huy_Click(self):
        self.ClearInput()  
        self.btnDat.config(state = "disabled")
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
        # Tiêu đề
        tk.Label(self, text="ĐẶT DỊCH VỤ", font=("Arial", 20, "bold"),
                 fg="#FFAA78", bg="Black").place(x=450, y=5, anchor="n", width=700, height=40)

        # Frame thông tin
        group = tk.LabelFrame(self, text="Thông tin đặt dịch vụ", font=("Arial", 10),
                              bg="#000000", fg="#0DFF00")
        group.place(relx=0.005, rely=0.23, anchor="w", width=300, height=170)

        # Entry & Label
        tk.Label(group, text="Mã đặt dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=5)
        self.entry_maddv = tk.Entry(group, font=("Arial", 10), state="disabled")
        self.entry_maddv.place(x=120, y=5, width=160, height=20)

        tk.Label(group, text="Mã đặt phòng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=35)
        self.entry_madp = tk.Entry(group, font=("Arial", 10), state="disabled")
        self.entry_madp.place(x=120, y=35, width=160, height=20)

        tk.Label(group, text="Mã dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=65)
        self.entry_madv = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_madv.place(x=120, y=65, width=160, height=20)

        tk.Label(group, text="Số lượng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=10, y=95)
        self.entry_sl = tk.Entry(group, font=("Arial", 10))
        self.entry_sl.place(x=120, y=95, width=160, height=20)

        # Bảng dịch vụ
        frame_dv = tk.Frame(self, bg="black")
        frame_dv.place(x=320, y=62, width=570, height=170)
        self.dichvu = ttk.Treeview(frame_dv, columns=("MaDV", "TenDV", "GiaDV"), show="headings")
        scroll_y = tk.Scrollbar(frame_dv, orient="vertical", command=self.dichvu.yview)
        scroll_x = tk.Scrollbar(frame_dv, orient="horizontal", command=self.dichvu.xview)
        self.dichvu.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.dichvu.heading("MaDV", text="Mã dịch vụ")
        self.dichvu.heading("TenDV", text="Tên dịch vụ")
        self.dichvu.heading("GiaDV", text="Giá dịch vụ")
        self.dichvu.column("MaDV", width=50)
        self.dichvu.column("TenDV", width=150)
        self.dichvu.column("GiaDV", width=100)
        self.dichvu.pack(fill="both", expand=True)
        # --- Chọn dòng ---
        self.dichvu.bind("<<TreeviewSelect>>", self.Chon_Dong_DichVu)

        # Bảng chi tiết dịch vụ
        frame_ctdv = tk.Frame(self, bg="black")
        frame_ctdv.place(x=10, y=250, width=880, height=170)
        self.ctdv = ttk.Treeview(frame_ctdv, columns=("MaCTDV", "MaDatPhong", "MaDV", "SoLuong"), show="headings")
        scroll_y2 = tk.Scrollbar(frame_ctdv, orient="vertical", command=self.ctdv.yview)
        scroll_x2 = tk.Scrollbar(frame_ctdv, orient="horizontal", command=self.ctdv.xview)
        self.ctdv.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)
        scroll_y2.pack(side="right", fill="y")
        scroll_x2.pack(side="bottom", fill="x")
        self.ctdv.heading("MaCTDV", text="Mã CTDV")
        self.ctdv.heading("MaDatPhong", text="Mã đặt phòng")
        self.ctdv.heading("MaDV", text="Mã dịch vụ")
        self.ctdv.heading("SoLuong", text="Số lượng")
        self.ctdv.column("MaCTDV", width=80)
        self.ctdv.column("MaDatPhong", width=150)
        self.ctdv.column("MaDV", width=150)
        self.ctdv.column("SoLuong", width=100)
        self.ctdv.pack(fill="both", expand=True)

        # Nút chức năng
        self.btnNhap = tk.Button(self, text="Nhập thông tin", font=("Arial", 12), fg="white", bg="#001f4d", command = self.NhapThongTin_Click)
        self.btnNhap.place(x=10, y=440, width=120, height=30)

        self.btnDat = tk.Button(self, text="Đặt", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Dat_Click)
        self.btnDat.place(x=260, y=440, width=120, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Huy_Click)
        self.btnHuy.place(x=510, y=440, width=120, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=760, y=440, width=120, height=30)