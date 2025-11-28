import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
from tkcalendar import DateEntry        # Dùng DateEntry
import pyodbc           # Kết nối Database

class Customer_Manage(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("QUẢN LÝ KHÁCH HÀNG")

        self.transient(parent)
        self.grab_set()

        # Đánh dấu thao tác Thêm = 1, Sửa = 2
        self.thaotac = 0

        # Kích thước form
        self.window_width = 900
        self.window_height = 600

        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Lấy vị trí ở giữa
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        # Đặt kích thước và vị trí
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.configure(bg="#000000")   # Chỉnh màu nền của form

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        self.connect_database()
        self.Load_Database_KhachHang()

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
    def Load_Database_KhachHang(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaKH, TenKH, CCCD, GioiTinh, SoDienThoai, QuocTich
                          FROM KhachHang''')
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ
        for i in self.khachhang.get_children():
            self.khachhang.delete(i)

        # Thêm dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.khachhang.insert("", tk.END, values=clean_row)

        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()
            
    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # ============================= CLEAR INPUT =============================
    def ClearInput(self):
        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")
        self.entry_cccd.config(state="normal")
        self.entry_sdt.config(state="normal")
        self.entry_quoctich.config(state="normal")

        self.entry_makh.delete(0, tk.END)
        self.entry_tenkh.delete(0, tk.END)
        self.entry_cccd.delete(0, tk.END)
        self.entry_sdt.delete(0, tk.END)
        self.entry_quoctich.delete(0, tk.END)

        self.selected_option.set("")  # reset radio button

    # ---Kiểm tra Số điện thoại ---
    def Check_Sdt(self, sdt):
        if len(sdt) == 10 and sdt.isdigit():
            return True
        else:
            return False

    # --- Kiểm tra trùng Số điện thoại ---  
    def Check_TrungSdt(self, sdt):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE SoDienThoai = ?", (sdt,))
        count_sdt = cursor.fetchone()[0]
        conn.close()
        if count_sdt > 0:
            return True
        return False
        
    # --- Kiểm tra CCCD
    def Check_Cccd(self, cccd):
        if len(cccd) == 12 and cccd.isdigit():
            return True
        else:
            return False
        
    # --- Kiểm tra trùng CCCD ---
    def Check_TrungCccd(self, cccd):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE CCCD = ?", (cccd,))
        count_cccd = cursor.fetchone()[0]
        conn.close()
        if count_cccd > 0:
            return True
        return False
    
    # --- Kiểm tra trùng Mã khách hàng ---
    def Check_TrungMaKH(self, makh: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM KhachHang WHERE MaKH = ?", (makh,))
        count_cccd = cursor.fetchone()[0]
        conn.close()
        if count_cccd > 0:
            return True
        return False 

    # ============================= CHỌN DÒNG =============================
    def Chon_Dong(self, event):
        if self.thaotac != 0:
            return  # đang thêm hoặc sửa thì không tự fill

        selected = self.khachhang.selection()
        if selected:
            item = self.khachhang.item(selected[0])["values"]

            self.entry_makh.config(state="normal")
            self.entry_makh.delete(0, tk.END)
            self.entry_makh.insert(0, item[0])
            self.entry_makh.config(state="readonly")

            self.entry_tenkh.config(state="normal")
            self.entry_tenkh.delete(0, tk.END)
            self.entry_tenkh.insert(0, item[1])
            self.entry_tenkh.config(state="readonly")

            self.entry_cccd.config(state="normal")
            self.entry_cccd.delete(0, tk.END)
            self.entry_cccd.insert(0, item[2])
            self.entry_cccd.config(state="readonly")

            # --- Giới tính ---
            if item[3] in ("Nam", "Nữ"):
                self.selected_option.set(item[3])
            else:
                self.selected_option.set("")  # không chọn gì nếu dữ liệu lạ

            self.entry_sdt.config(state="normal")
            self.entry_sdt.delete(0, tk.END)
            self.entry_sdt.insert(0, item[4])
            self.entry_sdt.config(state="readonly")

            self.entry_quoctich.config(state="normal")
            self.entry_quoctich.delete(0, tk.END)
            self.entry_quoctich.insert(0, item[5])
            self.entry_quoctich.config(state="readonly")
    
    # --- Kiểm tra khách hàng còn sử dụng phòng nào khách không ---
    def KhachHang_DaSuDungPhong(self, makh: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM DatPhong WHERE MaKH = ?''', (makh,))
        count = cursor.fetchone()[0]
        conn.close()
        if count > 0:
            return True
        return False
    
    # ============================= THÊM =============================
    def Them_Click(self):
        self.thaotac = 1
        self.ClearInput()
        self.entry_makh.focus_set()

        self.entry_makh.config(state="normal")
        self.entry_tenkh.config(state="normal")
        self.entry_cccd.config(state="normal")
        self.entry_sdt.config(state="normal")
        self.entry_quoctich.config(state="normal")

        self.btnLuu.config(state="normal")
        self.btnHuy.config(state="normal")

    # ============================= SỬA =============================
    def Sua_Click(self):
        selected = self.khachhang.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn khách hàng để cập nhật!")
            return

        self.thaotac = 2
        item = self.khachhang.item(selected[0])["values"]

        self.ClearInput()

        self.entry_makh.insert(0, item[0])
        self.entry_tenkh.insert(0, item[1])
        self.entry_cccd.insert(0, item[2])
        # --- Giới tính ---
        if item[3] in ("Nam", "Nữ"):
            self.selected_option.set(item[3])
        else:
            self.selected_option.set("")        
        self.entry_sdt.insert(0, item[4])
        self.entry_quoctich.insert(0, item[5])

        self.entry_makh.config(state="readonly")
        self.btnLuu.config(state="normal")
        self.btnHuy.config(state="normal")    # đóng lại vì nếu bấm dô là en try bay dữ liệu hết

    # ============================= XÓA =============================
    def Xoa_Click(self):
        selected = self.khachhang.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn khách hàng cần xóa!")
            return

        item = self.khachhang.item(selected[0])["values"]
        makh = item[0]
        self.ClearInput()

        self.entry_makh.insert(0, item[0])
        self.entry_tenkh.insert(0, item[1])
        self.entry_cccd.insert(0, item[2])
        if not messagebox.askyesno("Xác nhận", f"Bạn muốn xóa khách hàng {makh}?"):
            return

        if self.KhachHang_DaSuDungPhong(makh):
            messagebox.showerror("Lỗi", "Khách hàng vẫn còn đặt phòng khách. Không thể xóa!")
            return
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KhachHang WHERE MaKH = ?", (makh,))
        conn.commit()
        conn.close()

        self.Load_Database_KhachHang()

    # ============================= LƯU =============================
    def Luu_Click(self):
        makh = self.entry_makh.get().strip()
        tenkh = self.entry_tenkh.get().strip()
        cccd = self.entry_cccd.get().strip()
        gioitinh = self.selected_option.get().strip()
        sdt = self.entry_sdt.get().strip()
        quoctich = self.entry_quoctich.get().strip()

        if not makh or not tenkh or not cccd or not gioitinh or not sdt or not quoctich:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if self.thaotac == 1:
            if self.Check_TrungMaKH(makh):
                messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại trong hệ thống!")
                return
            if self.Check_TrungSdt(sdt):
                messagebox.showerror("Lỗi", "Số điện thoại đã tồn tại trong hệ thống!")
                return
            if self.Check_TrungCccd(cccd):
                messagebox.showerror("Lỗi", "CCCD đã tồn tại trong hệ thống!")
                return
        if not self.Check_Sdt(sdt):
            messagebox.showerror("Lỗi", "Số điện thoại phải là số và có đúng 10 chữ số!")
            return
        if not self.Check_Cccd(cccd):
            messagebox.showerror("Lỗi", "CCCD phải là số và có đúng 12 chữ số!")
            return
        
        
        conn = self.connect_database()
        cursor = conn.cursor()

        if self.thaotac == 1:   # thêm
            try:
                cursor.execute(
                    "INSERT INTO KhachHang VALUES (?, ?, ?, ?, ?, ?)",
                    (makh, tenkh, cccd, gioitinh, sdt, quoctich)
                )
                conn.commit()
                messagebox.showinfo("Thông báo", f"Thêm khách hàng {makh} thành công!")
            except pyodbc.IntegrityError:
                messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Thêm khách hàng thất bại:\n{e}")

        elif self.thaotac == 2:  # sửa
            cursor.execute(
                "UPDATE KhachHang SET TenKH=?, CCCD=?, GioiTinh=?, SoDienThoai=?, QuocTich=? WHERE MaKH=?",
                (tenkh, cccd, gioitinh, sdt, quoctich, makh)
            )
            conn.commit()
            messagebox.showinfo("Thông báo", f"Cập nhật khách hàng {makh} thành công!")

        conn.close()
        self.Load_Database_KhachHang()
        self.Huy_Click()
        self.thaotac = 0

    # ============================= HỦY =============================
    def Huy_Click(self):
        self.ClearInput()
        self.entry_makh.config(state="readonly")
        self.entry_tenkh.config(state="readonly")
        self.entry_cccd.config(state="readonly")
        self.entry_sdt.config(state="readonly")
        self.entry_quoctich.config(state="readonly")

        self.btnLuu.config(state="disabled")
        self.btnHuy.config(state="disabled")

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

        # ----------------------------- Tên form -----------------------------
        title_label = tk.Label(
            self, text="QUẢN LÝ KHÁCH HÀNG",
            font=("Arial", 20, "bold"), fg="#FFAA78", bg="Black"
        )
        title_label.place(x=450, y=5, anchor="n", width=700, height=40)

        # ----------------------------- Frame thông tin -----------------------------
        group = tk.LabelFrame(self, text="Thông tin khách hàng",
                              font=("Arial", 10), fg="#0DFF00", bg="#000000")
        group.place(relx=0.005, rely=0.22, anchor="w", width=560, height=140)

        # --- Mã khách hàng ---
        tk.Label(group, text="Mã khách hàng", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_makh = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_makh.place(x=115, y=5, width=160, height=20)

        # --- Họ tên khách hàng ---
        tk.Label(group, text="Họ tên", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_tenkh = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_tenkh.place(x=115, y=35, width=160, height=20)

        # --- CCCD ---
        tk.Label(group, text="CCCD", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.entry_cccd = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_cccd.place(x=115, y=65, width=160, height=20)

        # --- Giới tính khách hàng ---
        tk.Label(group, text="Giới tính", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=300, y=5)
        self.selected_option = tk.StringVar()
        rdbNam = tk.Radiobutton(group, text="Nam", variable=self.selected_option,
                                value="Nam", font=("Arial", 10),
                                fg="#FCBD00", bg="#000000")
        rdbNu = tk.Radiobutton(group, text="Nữ", variable=self.selected_option,
                               value="Nữ", font=("Arial", 10),
                               fg="#FCBD00", bg="#000000")
        rdbNam.place(x=370, y=5)
        rdbNu.place(x=440, y=5)

        # --- Số điện thoại khách hàng ---
        tk.Label(group, text="SĐT", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=300, y=35)
        self.entry_sdt = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_sdt.place(x=370, y=35, width=160, height=20)

        # --- Quốc tịch ---
        tk.Label(group, text="Quốc tịch", font=("Arial", 10),
                 fg="#FCBD00", bg="#000000").place(x=300, y=65)
        self.entry_quoctich = tk.Entry(group, font=("Arial", 10), state="readonly")
        self.entry_quoctich.place(x=370, y=65, width=160, height=20)

        # ----------------------------- Bảng khách hàng -----------------------------
        frame_table = tk.Frame(self, bg="black")
        frame_table.place(x=10, y=220, width=880, height=250)

        self.khachhang = ttk.Treeview(
            frame_table,
            columns=("MaKH", "TenKH", "CCCD", "GioiTinh", "SoDienThoai", "QuocTich"),
            show="headings"
        )

        scroll_y = tk.Scrollbar(frame_table, orient="vertical", command=self.khachhang.yview)
        scroll_x = tk.Scrollbar(frame_table, orient="horizontal", command=self.khachhang.xview)

        self.khachhang.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.khachhang.pack(fill="both", expand=True)

        # Chọn dòng
        self.khachhang.bind("<<TreeviewSelect>>", self.Chon_Dong)

        # Khai báo các cột
        self.khachhang.heading("MaKH", text="Mã khách hàng")
        self.khachhang.heading("TenKH", text="Tên khách hàng")
        self.khachhang.heading("CCCD", text="CCCD")
        self.khachhang.heading("GioiTinh", text="Giới tính")
        self.khachhang.heading("SoDienThoai", text="Số điện thoại")
        self.khachhang.heading("QuocTich", text="Quốc tịch")

        self.khachhang.column("MaKH", width=100)
        self.khachhang.column("TenKH", width=210)
        self.khachhang.column("CCCD", width=140)
        self.khachhang.column("GioiTinh", width=70)
        self.khachhang.column("SoDienThoai", width=140)
        self.khachhang.column("QuocTich", width=200)

        # ============================= Chức năng (Thêm Xoá Sửa ...) =============================
        # --- Thêm ---
        self.btnThem = tk.Button(self, text="Thêm", font=("Arial", 12),
                                 fg="white", bg="#001f4d", command=self.Them_Click)
        self.btnThem.place(x=580, y=70, width=90, height=30)

        # --- Xoá ---
        self.btnXoa = tk.Button(self, text="Xoá", font=("Arial", 12),
                                fg="white", bg="#001f4d", command=self.Xoa_Click)
        self.btnXoa.place(x=680, y=70, width=90, height=30)

        # --- Sửa ---
        self.btnSua = tk.Button(self, text="Sửa", font=("Arial", 12),
                                fg="white", bg="#001f4d", command=self.Sua_Click)
        self.btnSua.place(x=780, y=70, width=90, height=30)

        # --- Huỷ ---
        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12),
                                fg="white", bg="#001f4d", state="disabled", command = self.Huy_Click)
        self.btnHuy.place(x=580, y=110, width=90, height=30)

        # --- Lưu ---
        self.btnLuu = tk.Button(self, text="Lưu", font=("Arial", 12),
                                fg="white", bg="#001f4d", state="disabled", command = self.Luu_Click)
        self.btnLuu.place(x=680, y=110, width=90, height=30)

        # --- Thoát ---
        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12),
                                  fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=780, y=110, width=90, height=30)