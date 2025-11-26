import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
import pyodbc           # Kết nối Database

class Service_Manage(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("QUẢN LÝ DỊCH VỤ")

        # Đánh dấu thao tác (1 = thêm, 2 = sửa)
        self.thaotac = 0

        # Kích thước form
        window_width = 900
        window_height = 600

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
        self.Load_Database_DichVu()

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

    # ----------------------------- Load CSDL -----------------------------
    def Load_Database_DichVu(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaDV, TenDV, GiaDV FROM DichVu''')
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.dichvu.get_children():
            self.dichvu.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.dichvu.insert("", tk.END, values=clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()
            
    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # ============================= CLEAR INPUT =============================
    def ClearInput(self):
        self.entry_madv.delete(0, tk.END)
        self.entry_tendv.delete(0, tk.END)
        self.entry_giadv.delete(0, tk.END)

    # ============================= CHỌN DÒNG =============================
    def Chon_Dong(self, event):
        if self.thaotac != 0:
            return

        selected = self.dichvu.selection()
        if selected:
            item = self.dichvu.item(selected[0])["values"]

            self.entry_madv.config(state="normal")
            self.entry_madv.delete(0, tk.END)
            self.entry_madv.insert(0, item[0])
            self.entry_madv.config(state="readonly")

            self.entry_tendv.config(state="normal")
            self.entry_tendv.delete(0, tk.END)
            self.entry_tendv.insert(0, item[1])
            self.entry_tendv.config(state="readonly")

            self.entry_giadv.config(state="normal")
            self.entry_giadv.delete(0, tk.END)
            self.entry_giadv.insert(0, item[2])
            self.entry_giadv.config(state="readonly")
    
    # --- Kiểm tra dịch vụ đã được sử dụng không ---
    def Check_DVDaSuDung(self, madv: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM ChiTietDichVu WHERE MaDV = ?''', (madv,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False

    # --- Kiểm tra trùng mã dịch vụ ---
    def Check_TrungMaDV(self, madv: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM DichVu WHERE MaDV = ?''', (madv,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False

    # ============================= THÊM =============================
    def Them_Click(self):
        self.thaotac = 1
        self.ClearInput()
        self.entry_madv.focus_set()

        self.entry_madv.config(state="normal")
        self.entry_tendv.config(state="normal")
        self.entry_giadv.config(state="normal")

        self.btnLuu.config(state="normal")
        self.btnHuy.config(state="normal")

    # ============================= SỬA =============================
    def Sua_Click(self):
        selected = self.dichvu.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn dịch vụ để sửa!")
            return

        self.thaotac = 2
        item = self.dichvu.item(selected[0])["values"]

        self.ClearInput()

        self.entry_madv.insert(0, item[0])
        self.entry_tendv.insert(0, item[1])
        self.entry_giadv.insert(0, item[2])

        self.entry_madv.config(state="readonly")  # Mã DV không cho sửa
        self.entry_tendv.config(state="normal")
        self.entry_giadv.config(state="normal")

        self.btnLuu.config(state="normal")
        self.btnHuy.config(state="normal")

    # ============================= XÓA =============================
    def Xoa_Click(self):
        selected = self.dichvu.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn dịch vụ cần xóa!")
            return

        item = self.dichvu.item(selected[0])["values"]
        madv = item[0]
        self.ClearInput()

        self.entry_madv.insert(0, item[0])
        self.entry_tendv.insert(0, item[1])
        self.entry_giadv.insert(0, item[2])

        self.entry_madv.config(state="readonly")  # Mã DV không cho sửa
        self.entry_tendv.config(state="normal")
        self.entry_giadv.config(state="normal")

        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa dịch vụ {madv}?")
        if not result:
            return

        if self.Check_DVDaSuDung(madv):
            messagebox.showerror("Lỗi", "Dịch vụ đã được sử dụng. Không thể xóa!")
            return
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DichVu WHERE MaDV = ?", (madv,))
        conn.commit()
        conn.close()

        self.Load_Database_DichVu()

    # ============================= LƯU =============================
    def Luu_Click(self):
        madv = self.entry_madv.get().strip()
        tendv = self.entry_tendv.get().strip()
        giadv = self.entry_giadv.get().strip()

        if not madv or not tendv or not giadv:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if self.thaotac == 1:
            if self.Check_TrungMaDV(madv):
                messagebox.showwarning("Thông báo", "Mã dịch vụ đã tồn tại trong hệ thống!")
                return
        if not giadv.isdigit():
            messagebox.showerror("Lỗi", "Tiền phòng phải là số!")
            return
        conn = self.connect_database()
        cursor = conn.cursor()

        # --- Thêm ---
        if self.thaotac == 1:
            try:
                cursor.execute(
                    "INSERT INTO DichVu VALUES (?, ?, ?)",
                    (madv, tendv, giadv)
                )
                conn.commit()
                messagebox.showinfo("Thông báo", f"Thêm dịch vụ {madv} thành công!")
            except:
                messagebox.showerror("Lỗi", "Mã dịch vụ đã tồn tại!")

        # --- Sửa ---
        elif self.thaotac == 2:
            cursor.execute(
                "UPDATE DichVu SET TenDV=?, GiaDV=? WHERE MaDV=?",
                (tendv, giadv, madv)
            )
            conn.commit()
            messagebox.showinfo("Thông báo", f"Cập nhật dịch vụ {madv} thành công!")

        conn.close()
        self.Load_Database_DichVu()
        self.Huy_Click()
        self.thaotac = 0

    # ============================= HỦY =============================
    def Huy_Click(self):
        self.ClearInput()

        self.entry_madv.config(state="readonly")
        self.entry_tendv.config(state="readonly")
        self.entry_giadv.config(state="readonly")

        self.btnLuu.config(state="disabled")
        self.btnHuy.config(state="disabled")

        self.thaotac = 0

    # ======================= THOÁT =======================
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()  # hiện lại form cha
            self.destroy()

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):

        # ----------------------------- Tên form -----------------------------
        title_label = tk.Label(self, text="QUẢN LÝ DỊCH VỤ",
                               font=("Arial", 20, "bold"),
                               fg="#FFAA78", bg="Black")
        title_label.place(x=450, y=5, anchor="n", width=700, height=40)

        # ----------------------------- Frame thông tin -----------------------------
        group = tk.LabelFrame(self, text="Thông tin dịch vụ", font=("Arial", 10),
                              fg="#0DFF00", bg="#000000")
        group.place(x=10, y=130, anchor="w", width=300, height=150)

        # --- Mã dịch vụ ---
        tk.Label(group, text="Mã dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_madv = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_madv.place(x=110, y=5, width=160, height=20)

        # --- Tên dịch vụ ---
        tk.Label(group, text="Tên dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_tendv = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_tendv.place(x=110, y=35, width=160, height=20)

        # --- Giá dịch vụ ---
        tk.Label(group, text="Tiền dịch vụ", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_giadv = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_giadv.place(x=110, y=65, width=160, height=20)

        # ----------------------------- Bảng dịch vụ -----------------------------
        frame_table = tk.Frame(self, bg="black")
        frame_table.place(x=320, y=65, width=550, height=230)

        self.dichvu = ttk.Treeview(
            frame_table,
            columns=("MaDV", "TenDV", "GiaDV"),
            show="headings"
        )

        scroll_y = tk.Scrollbar(frame_table, orient="vertical", command=self.dichvu.yview)
        scroll_x = tk.Scrollbar(frame_table, orient="horizontal", command=self.dichvu.xview)

        self.dichvu.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.dichvu.pack(fill="both", expand=True)

        self.dichvu.heading("MaDV", text="Mã dịch vụ")
        self.dichvu.heading("TenDV", text="Tên dịch vụ")
        self.dichvu.heading("GiaDV", text="Giá dịch vụ")

        self.dichvu.column("MaDV", width=80)
        self.dichvu.column("TenDV", width=200)
        self.dichvu.column("GiaDV", width=100)

        # Chọn dòng
        self.dichvu.bind("<<TreeviewSelect>>", self.Chon_Dong)

        # ============================= Các nút chức năng =============================
        self.btnThem = tk.Button(self, text="Thêm", font=("Arial", 12),
                                 fg="white", bg="#001f4d",
                                 command=self.Them_Click)
        self.btnThem.place(x=10, y=210, width=90, height=30)

        self.btnXoa = tk.Button(self, text="Xoá", font=("Arial", 12),
                                fg="white", bg="#001f4d",
                                command=self.Xoa_Click)
        self.btnXoa.place(x=115, y=210, width=90, height=30)

        self.btnSua = tk.Button(self, text="Sửa", font=("Arial", 12),
                                fg="white", bg="#001f4d",
                                command=self.Sua_Click)
        self.btnSua.place(x=220, y=210, width=90, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12),
                                fg="white", bg="#001f4d",
                                state="disabled", command=self.Huy_Click)
        self.btnHuy.place(x=10, y=250, width=90, height=30)

        self.btnLuu = tk.Button(self, text="Lưu", font=("Arial", 12),
                                fg="white", bg="#001f4d",
                                state="disabled", command=self.Luu_Click)
        self.btnLuu.place(x=115, y=250, width=90, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                                  fg="white", bg="#001f4d",
                                  command=self.Thoat_Click)
        self.btnThoat.place(x=220, y=250, width=90, height=30)