import tkinter as tk
from tkinter import ttk, messagebox    #Dùng combobox, messagebox
import pyodbc           # Kết nối Database
from tkcalendar import DateEntry    #Dùng DateEntry
import datetime

class Staff_Manage(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.thaotac = 0       # Đánh dấu thao tác Thêm = 1 && Sửa = 2
        self.title("QUẢN LÝ NHÂN SỰ")
        self.configure(bg="#000000")

        # Kích thước form
        window_width = 900
        window_height = 600

        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Lấy vị trí ở giữa
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        # Load dữ liệu vào bảng
        self.Load_Database_NhanSu()

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

    # ============================= Load dữ liệu =============================
    def Load_Database_NhanSu(self):
        conn = self.connect_database()
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute('''SELECT MaNV, TenNV, NgaySinh, GioiTinh, SoDienThoai, ChucVu
                          FROM NhanVien''')
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
            
    # =============================================== SỰ KIỆN ===============================================
    # =======================================================================================================
    # --- ClearInput ---
    def ClearInput(self):  
        self.entry_manv.config(state="normal")
        self.entry_tennv.config(state="normal")
        self.ngaysinh.config(state="normal")
        self.entry_sdt.config(state="normal")
        self.cbo_chucvu.config(state="readonly")  # Combobox nên để readonly  

        self.entry_manv.delete(0, tk.END)
        self.entry_tennv.delete(0, tk.END)
        self.ngaysinh.set_date(datetime.date.today())
        self.selected_option.set("")      # Reset Radiobutton Nam - Nữ
        self.entry_sdt.delete(0, tk.END)
        self.cbo_chucvu.set("")

    # --- Chọn dòng ---
    def Chon_Dong(self, event):
        selected = self.nhansu.selection()
        if not selected:
            return

        item = self.nhansu.item(selected[0])["values"]

        # Mã NV
        self.entry_manv.config(state="normal")
        self.entry_manv.delete(0, tk.END)
        self.entry_manv.insert(0, item[0])
        self.entry_manv.config(state="readonly")

        # Họ tên
        self.entry_tennv.config(state="normal")
        self.entry_tennv.delete(0, tk.END)
        self.entry_tennv.insert(0, item[1])
        self.entry_tennv.config(state="readonly")

        # Ngày sinh
        try:
            if isinstance(item[2], str):
                ngay = datetime.datetime.strptime(item[2], "%Y-%m-%d").date()
            else:
                ngay = item[2]
            self.ngaysinh.set_date(ngay)
        except:
            self.ngaysinh.set_date(datetime.date.today())

        # Giới tính
        self.selected_option.set(item[3] if item[3] in ("Nam", "Nữ") else "")

        # SĐT
        self.entry_sdt.config(state="normal")
        self.entry_sdt.delete(0, tk.END)
        self.entry_sdt.insert(0, item[4])
        self.entry_sdt.config(state="readonly")

        # Chức vụ
        self.cbo_chucvu.config(state="normal")
        self.cbo_chucvu.set(item[5])
        self.cbo_chucvu.config(state="readonly")

    # ---Kiểm tra Số điện thoại ---
    def Check_Sdt(self, sdt):
        if len(sdt) == 10 and sdt.isdigit():
            return True
        else:
            return False
    
    # ---Kiểm tra trùng Số điện thoại ---
    def Check_TrungSdt(self, sdt):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE SoDienThoai = ?", (sdt,))
        count_sdt = cursor.fetchone()[0]
        conn.close()
        if count_sdt > 0:
            return True
        return False

    # ---Kiểm tra trùng mã nhân viên ---    
    def Check_TrungMaNV(self, manv: str):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM NhanVien WHERE MaNV = ?", (manv,))
        count_sdt = cursor.fetchone()[0]
        conn.close()
        if count_sdt > 0:
            return True
        return False
    # ======================= THÊM =======================
    def Them_Click(self):
        self.ClearInput()
        self.thaotac = 1
        self.entry_manv.focus_set()

        self.entry_manv.config(state = "normal")
        self.entry_tennv.config(state = "normal")
        self.ngaysinh.config(state = "normal")
        self.entry_sdt.config(state = "normal")

        self.btnLuu.config(state = "normal")
        self.btnHuy.config(state = "normal")

    # ======================= SỬA =======================
    def Sua_Click(self):
        selected = self.nhansu.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn nhân viên để cập nhật")
            return

        self.thaotac = 2
        item = self.nhansu.item(selected[0])["values"]

        self.ClearInput()

        # Điền dữ liệu từ Treeview
        self.entry_manv.insert(0, item[0])
        self.entry_tennv.insert(0, item[1])
        # --- Ngày sinh ---
        try:
            # Nếu item[2] là chuỗi 'YYYY-MM-DD' hoặc 'DD/MM/YYYY'
            if isinstance(item[2], str):
                try:
                    ngaysinh_dt = datetime.datetime.strptime(item[2], "%Y-%m-%d").date()
                except:
                    ngaysinh_dt = datetime.datetime.strptime(item[2], "%d/%m/%Y").date()
            else:
                ngaysinh_dt = item[2]  # nếu đã là datetime.date
            self.ngaysinh.set_date(ngaysinh_dt)
        except Exception as e:
            self.ngaysinh.set_date(datetime.date.today())

        # --- Giới tính ---
        if item[3] in ("Nam", "Nữ"):
            self.selected_option.set(item[3])
        else:
            self.selected_option.set("")

        self.entry_sdt.insert(0, str(item[4]))
        self.cbo_chucvu.set(str(item[5]))

        self.entry_manv.config(state="readonly")
        self.btnHuy.config(state="normal")
        self.btnLuu.config(state="normal")
    
    # ======================= XÓA =======================
    def Xoa_Click(self):
        selected = self.nhansu.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Bạn chưa chọn nhân viên để xóa")
            return
        
        item = self.nhansu.item(selected[0])["values"]
        manv = item[0]   # Lấy mã nhân viên

        if not messagebox.askyesno("Xác nhận", f"Bạn muốn xóa nhân viên {manv}?"):
            return

        conn = self.connect_database()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM NhanVien WHERE MaNV = ?", (manv,))
        conn.commit()
        conn.close()
        self.Load_Database_NhanSu()

    # ======================= Lưu =======================
    def Luu_Click(self):
        manv = self.entry_manv.get().strip()
        tennv = self.entry_tennv.get().strip()
        ngaysinh = self.ngaysinh.get_date()  # Lấy ngày từ DateEntry
        gioitinh = self.selected_option.get()   # Lấy giá trị giới tính
        sdt = self.entry_sdt.get().strip()
        chucvu = self.cbo_chucvu.get().strip()

        if not manv or not tennv or not ngaysinh or not gioitinh or not sdt or not chucvu:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if self.thaotac == 1:
            if self.Check_TrungMaNV(manv):
                messagebox.showerror("Lỗi", "Mã nhân viên đã tồn tại trong hệ thống!")
                return
        if not self.Check_Sdt(sdt):
            messagebox.showerror("Lỗi", "Số điện thoại phải là số và có đúng 10 chữ số!")
            return
        if self.Check_TrungSdt(sdt):
            messagebox.showerror("Lỗi", "Số điện thoại đã tồn tại trong hệ thống!")
            return

        conn = self.connect_database()
        cursor = conn.cursor()

        if self.thaotac == 1:  # Thêm
            try:
                cursor.execute("INSERT INTO NhanVien (MaNV, TenNV, NgaySinh, GioiTinh, SoDienThoai, ChucVu) VALUES (?, ?, ?, ?, ?, ?)"
                            , (manv, tennv, ngaysinh, gioitinh, sdt, chucvu))
                conn.commit()
                messagebox.showinfo("Thông báo", f"Thêm nhân viên {manv} thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Mã nhân viên đã tồn tại hoặc lỗi khác:\n{e}")

        elif self.thaotac == 2:  # Sửa
            cursor.execute("UPDATE NhanVien SET TenNV=?, NgaySinh=?, GioiTinh=?, SoDienThoai=?, ChucVu=? "
                           "WHERE MaNV=?", (tennv, ngaysinh, gioitinh, sdt, chucvu, manv))
            conn.commit()
            messagebox.showinfo("Thông báo", f"Cập nhật nhân viên {manv} thành công!")
        conn.close()
        # Cập nhật lại Treeview và reset form
        self.Load_Database_NhanSu()
        self.ClearInput()
        self.btnHuy.config(state="disabled")
        self.btnLuu.config(state="disabled")
        self.thaotac = 0

    # ======================= HỦY =======================
    def Huy_Click(self):
        self.ClearInput()
        self.entry_manv.focus_set()

        self.entry_manv.config(state="readonly") 
        self.entry_tennv.config(state="readonly")
        self.entry_sdt.config(state="readonly")
        self.ngaysinh.config(state="disabled")

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
        # Tên form
        title_label = tk.Label(self, text="QUẢN LÝ NHÂN SỰ", 
                               font=("Arial", 20, "bold"),
                               fg="#FFAA78", bg="Black")
        title_label.place(x=450, y=5, anchor="n", width=700, height=40)

        # Thông tin nhân sự
        group = tk.LabelFrame(self, text="Thông tin nhân sự", font=("Arial", 10),
                              fg="#0DFF00", bg="#000000")
        group.place(relx=0.005, rely=0.22, anchor="w", width=560, height=140)

        # --- Mã nhân viên ---
        tk.Label(group, text="Mã nhân viên", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=5)
        self.entry_manv = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_manv.place(x=110, y=5, width=160, height=20)

        # --- Họ tên ---
        tk.Label(group, text="Họ tên", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=35)
        self.entry_tennv = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_tennv.place(x=110, y=35, width=160, height=20)

        # --- Ngày sinh ---
        tk.Label(group, text="Ngày sinh", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=20, y=65)
        self.ngaysinh = DateEntry(group, date_pattern="dd/mm/yyyy", state = "readonly")
        self.ngaysinh.place(x=110, y=65, width=160, height=20)

        # --- Giới tính ---
        tk.Label(group, text="Giới tính", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=300, y=5)
        self.selected_option = tk.StringVar()
        rdbNam = tk.Radiobutton(group, text="Nam", variable=self.selected_option, value="Nam", 
                                font=("Arial", 10), fg="#FCBD00", bg="#000000")
        rdbNu = tk.Radiobutton(group, text="Nữ", variable=self.selected_option, value="Nữ", 
                               font=("Arial", 10), fg="#FCBD00", bg="#000000")
        rdbNam.place(x=370, y=5)
        rdbNu.place(x=440, y=5)

        # --- SĐT ---
        tk.Label(group, text="SĐT", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=300, y=35)
        self.entry_sdt = tk.Entry(group, font=("Arial", 10), state = "readonly")
        self.entry_sdt.place(x=370, y=35, width=160, height=20)

        # --- Chức vụ ---
        tk.Label(group, text="Chức vụ", font=("Arial", 10), fg="#FCBD00", bg="#000000").place(x=300, y=65)
        combo_values = ["Quản lý", "Lễ tân", "Kế toán", "Thu ngân", 
                        "Nhân viên buồng phòng", "Nhân viên bảo trì", 
                        "Nhân viên phục vụ/ dịch vụ"]
        self.cbo_chucvu = ttk.Combobox(group, values=combo_values, font=("Arial", 10), state = "readonly")
        self.cbo_chucvu.place(x=370, y=65, width=160, height=20)

        # Bảng nhân sự
        frame_table = tk.Frame(self, bg="black")
        frame_table.place(x=10, y=220, width=880, height=250)

        self.nhansu = ttk.Treeview(frame_table,
                                   columns=("MaNV", "TenNV", "NgaySinh", "GioiTinh", "SoDienThoai", "ChucVu"),
                                   show="headings")

        # Scrollbar
        scroll_y = tk.Scrollbar(frame_table, orient="vertical", command=self.nhansu.yview)
        self.nhansu.configure(yscrollcommand=scroll_y.set)
        scroll_x = tk.Scrollbar(frame_table, orient="horizontal", command=self.nhansu.xview)
        self.nhansu.configure(xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.nhansu.pack(fill="both", expand=True)

        # Chọn dòng
        self.nhansu.bind("<<TreeviewSelect>>", self.Chon_Dong)

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

        # Nút chức năng
        self.btnThem = tk.Button(self, text="Thêm", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Them_Click)
        self.btnThem.place(x=580, y=70, width=90, height=30)

        self.btnXoa = tk.Button(self, text="Xoá", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Xoa_Click)
        self.btnXoa.place(x=680, y=70, width=90, height=30)

        self.btnSua = tk.Button(self, text="Sửa", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Sua_Click)
        self.btnSua.place(x=780, y=70, width=90, height=30)

        self.btnHuy = tk.Button(self, text="Huỷ", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled", command = self.Huy_Click)
        self.btnHuy.place(x=580, y=110, width=90, height=30)

        self.btnLuu = tk.Button(self, text="Lưu", font=("Arial", 12), fg="white", bg="#001f4d", state = "disabled",  command = self.Luu_Click)
        self.btnLuu.place(x=680, y=110, width=90, height=30)

        self.btnThoat = tk.Button(self, text="Thoát", font=("Arial", 12), fg="white", bg="#001f4d", command = self.Thoat_Click)
        self.btnThoat.place(x=780, y=110, width=90, height=30)