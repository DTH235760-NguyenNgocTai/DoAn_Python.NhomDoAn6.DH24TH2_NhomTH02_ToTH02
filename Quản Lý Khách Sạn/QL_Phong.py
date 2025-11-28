import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
import pyodbc           # Kết nối Database

class Room_Manage(tk.Toplevel):     
    def __init__(self, parent):
        super().__init__(parent)     # Gọi constructor của Toplevel
        self.parent = parent
        self.thaotac = 0       # Đánh dấu thao tác Thêm = 1 && Sửa = 2
        self.title("QUẢN LÝ PHÒNG")

        self.transient(parent)
        self.grab_set()

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
    def Load_Database_Phong(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT MaPhong, LoaiPhong, TrangThai, GiaTien FROM Phong")
        rows = cursor.fetchall()

        for item in self.phong.get_children():
            self.phong.delete(item)

        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]    # Xóa các kí tự '' và () trước khi đưa vào bảng
            self.phong.insert("", tk.END, values=clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()

    def ClearInput(self):
        self.entry_maphong.config(state="normal")
        self.entry_tienphong.config(state="normal")

        self.entry_maphong.delete(0, tk.END)
        self.cbo_loaiphong.set("")
        self.cbo_trangthai.set("")
        self.entry_tienphong.delete(0, tk.END)

    # ======================= CHỌN DÒNG =======================
    def Chon_Dong(self, event):
        if self.thaotac != 0:
            return  # khi đang Thêm hoặc Sửa → không auto fill

        selected = self.phong.selection()
        if selected:
            item = self.phong.item(selected[0])["values"]

            self.entry_maphong.config(state="normal")
            self.entry_maphong.delete(0, tk.END)
            self.entry_maphong.insert(0, item[0])
            self.entry_maphong.config(state="readonly")

            self.cbo_loaiphong.set(item[1])
            self.cbo_trangthai.set(item[2])

            self.entry_tienphong.config(state="normal")
            self.entry_tienphong.delete(0, tk.END)
            self.entry_tienphong.insert(0, item[3])
            self.entry_tienphong.config(state="readonly")
    
    # --- Kiểm tra phòng đã được sử dụng hay không
    def Phong_DaSuDung(self, maphong: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM DatPhong WHERE MaPhong = ?''', (maphong,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False
    
    def Check_TrungMaPhong(self, maphong: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM Phong WHERE MaPhong = ?''', (maphong,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False

    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # ======================= THÊM =======================
    def Them_Click(self):
        self.thaotac = 1
        self.ClearInput()
        self.entry_maphong.focus_set()
        self.entry_maphong.config(state="normal")
        self.entry_tienphong.config(state="normal")
        self.btnHuy.config(state="normal")
        self.btnLuu.config(state="normal")

    # ======================= SỬA =======================
    def Sua_Click(self):
        selected = self.phong.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng để cập nhật!")
            return

        self.thaotac = 2
        item = self.phong.item(selected[0])["values"]

        self.ClearInput()

        self.entry_maphong.insert(0, item[0])
        self.cbo_loaiphong.set(item[1])
        self.cbo_trangthai.set(item[2])
        self.entry_tienphong.insert(0, item[3])

        self.entry_maphong.config(state="readonly")

        self.btnHuy.config(state="normal")
        self.btnLuu.config(state="normal")

    # ======================= XÓA =======================
    def Xoa_Click(self):
        selected = self.phong.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn phòng cần xóa!")
            return

        item = self.phong.item(selected[0])["values"]
        maphong = item[0]  # Lấy mã phòng

        if not messagebox.askyesno("Xác nhận", f"Bạn muốn xóa phòng {maphong}?"):
            return
        if self.Phong_DaSuDung(maphong):
            messagebox.showerror("Lỗi", "Phòng đã được sử dụng. Không thể xóa!")
            return
        conn = self.connect_database()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Phong WHERE MaPhong = ?", (maphong,))
        conn.commit()
        conn.close()
        self.Load_Database_Phong()

    # ======================= LƯU =======================
    def Luu_Click(self):
        maphong = self.entry_maphong.get().strip()
        loaiphong = self.cbo_loaiphong.get().strip()
        trangthai = self.cbo_trangthai.get().strip()
        tienphong = self.entry_tienphong.get().strip()

        if not maphong or not loaiphong or not trangthai or not tienphong:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if self.thaotac == 1:
            if self.Check_TrungMaPhong(maphong):
                messagebox.showwarning("Thông báo", "Mã phòng đã tồn tại trong hệ thống!")
                return
        
        if not tienphong.isdigit():
            messagebox.showerror("Lỗi", "Tiền phòng phải là số!")
            return
        tienphong = int(tienphong)   # Ép kiểu giá tiền thành INT để đưa vào CSDL

        conn = self.connect_database()
        cursor = conn.cursor()

        if self.thaotac == 1:
            try:
                cursor.execute(
                    "INSERT INTO Phong VALUES (?, ?, ?, ?)",
                    (maphong, loaiphong, trangthai, tienphong)
                )
                conn.commit()
                messagebox.showinfo("Thông báo", f"Thêm phòng {maphong} thành công!")
            except:
                messagebox.showerror("Lỗi", "Mã phòng đã tồn tại!")

        elif self.thaotac == 2:
            cursor.execute(
                "UPDATE Phong SET LoaiPhong=?, TrangThai=?, GiaTien=? WHERE MaPhong=?",
                (loaiphong, trangthai, tienphong, maphong)
            )
            conn.commit()
            messagebox.showinfo("Thông báo", f"Cập nhật phòng {maphong} thành công!")

        conn.close()
        self.Load_Database_Phong()
        self.ClearInput()
        self.entry_maphong.config(state="readonly")
        self.entry_tienphong.config(state="readonly")
        self.btnHuy.config(state="disabled")
        self.btnLuu.config(state="disabled")
        self.thaotac = 0

    # ======================= HỦY =======================
    def Huy_Click(self):
        self.ClearInput()
        self.entry_maphong.focus_set()
        self.entry_maphong.config(state="readonly")
        self.entry_tienphong.config(state="readonly")
        self.btnHuy.config(state="disabled")
        self.btnLuu.config(state="disabled")
        self.thaotac = 0

    # ======================= THOÁT =======================
    def Thoat_Click(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            if self.parent:
                self.parent.deiconify()   # hiển thị lại form cha
            self.destroy()

    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):
        tk.Label(
            self,                            # <<=== self.root → self
            text="QUẢN LÝ PHÒNG",
            font=("Arial", 20, "bold"),
            fg="#FFAA78", bg="Black"
        ).place(x=450, y=5, anchor="n", width=700, height=40)

        group = tk.LabelFrame(
            self,                              # <<=== self.root → self
            text="Thông tin phòng",
            font=("Arial", 10), fg="#0DFF00", bg="#000000"
        )
        group.place(x=10, y=130, anchor="w", width=300, height=150)

        # ======================= LABEL & ENTRY =======================
        tk.Label(group, text="Mã phòng", fg="#FCBD00", bg="#000000", font=("Arial", 10)).place(x=20, y=5)
        self.entry_maphong = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_maphong.place(x=110, y=5, width=160, height=20)

        tk.Label(group, text="Loại phòng", fg="#FCBD00", bg="#000000", font=("Arial", 10)).place(x=20, y=35)
        loaiphong_values = ["Single Room", "Double Room", "Luxury Room", "VIP Room", "Meeting Room"]
        self.cbo_loaiphong = ttk.Combobox(group, values=loaiphong_values, font=("Arial", 10), state="readonly")
        self.cbo_loaiphong.place(x=110, y=35, width=160, height=20)

        tk.Label(group, text="Trạng thái", fg="#FCBD00", bg="#000000", font=("Arial", 10)).place(x=20, y=65)
        trangthai_values = ["Trống", "Đang thuê", "Đã đặt trước", "Bảo trì"]
        self.cbo_trangthai = ttk.Combobox(group, values=trangthai_values, font=("Arial", 10), state="readonly")
        self.cbo_trangthai.place(x=110, y=65, width=160, height=20)

        tk.Label(group, text="Tiền phòng", fg="#FCBD00", bg="#000000", font=("Arial", 10)).place(x=20, y=95)
        self.entry_tienphong = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_tienphong.place(x=110, y=95, width=160, height=20)

        # ======================= CÁC NÚT =======================
        self.btnThem = tk.Button(self, text="Thêm", font=("Arial", 12),
                  fg="white", bg="#001f4d", command=self.Them_Click)
        self.btnThem.place(x=10, y=210, width=90, height=30)

        self.btnXoa = tk.Button(self, text="Xoá", font=("Arial", 12),
                  fg="white", bg="#001f4d", command=self.Xoa_Click)
        self.btnXoa.place(x=115, y=210, width=90, height=30)

        self.btnSua = tk.Button(self, text="Sửa", font=("Arial", 12),
                  fg="white", bg="#001f4d", command=self.Sua_Click)
        self.btnSua.place(x=220, y=210, width=90, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12), state="disabled",
                  fg="white", bg="#001f4d", command=self.Huy_Click)
        self.btnHuy.place(x=10, y=250, width=90, height=30)

        self.btnLuu = tk.Button(self, text="Lưu", font=("Arial", 12), state="disabled",
                  fg="white", bg="#001f4d", command=self.Luu_Click)
        self.btnLuu.place(x=115, y=250, width=90, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                  fg="white", bg="#001f4d", command=self.Thoat_Click)
        self.btnThoat.place(x=220, y=250, width=90, height=30)

        frame_table = tk.Frame(self, bg="black")
        frame_table.place(x=320, y=65, width=550, height=230)

        # === Bảng phòng ===
        self.phong = ttk.Treeview(
            frame_table,
            columns=("MaPhong", "LoaiPhong", "TrangThai", "GiaTien"),
            show="headings"
        )

        scroll_y = tk.Scrollbar(frame_table, orient="vertical", command=self.phong.yview)
        scroll_x = tk.Scrollbar(frame_table, orient="horizontal", command=self.phong.xview)

        self.phong.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.phong.pack(fill="both", expand=True)

        # Chọn dòng
        self.phong.bind("<<TreeviewSelect>>", self.Chon_Dong)

        self.phong.heading("MaPhong", text="Mã phòng")
        self.phong.heading("LoaiPhong", text="Loại phòng")
        self.phong.heading("TrangThai", text="Trạng thái")
        self.phong.heading("GiaTien", text="Giá tiền")

        self.phong.column("MaPhong", width=80)
        self.phong.column("LoaiPhong", width=150)
        self.phong.column("TrangThai", width=150)
        self.phong.column("GiaTien", width=100)