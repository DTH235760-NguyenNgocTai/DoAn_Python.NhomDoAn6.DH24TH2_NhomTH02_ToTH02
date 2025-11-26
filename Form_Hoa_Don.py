import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
import datetime

class HoaDon(tk.Toplevel):
    def __init__(self, parent = None, madp = None, tenkh = None, maphong = None, loaiphong = None, giaphong = None, tongtienphong = None, tongtiendv = None, 
                 thanhtien = None, ngaynhan_dt = None, ngaytra_dt = None):
        super().__init__(parent)
        self.parent = parent
        self.madp = madp
        self.tenkh = tenkh
        self.maphong = maphong
        self.loaiphong = loaiphong
        self.giaphong = giaphong
        self.tongtienphong = tongtienphong
        self.tongtiendv = tongtiendv
        self.thanhtien = thanhtien
        self.ngaynhan_dt = ngaynhan_dt
        self.ngaytra_dt = ngaytra_dt

        self.title("Hoá đơn")
        self.geometry("750x500")
        self.configure(bg="white")

        # Bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.TaoGiaoDien()
        self.HienThiThongTinPhong()
        self.HienThiThongTinDV()

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
        
    # ============================= Thông tin phòng =============================
    def HienThiThongTinPhong(self):
        self.entry_tenkh.insert(0, str(self.tenkh))
        self.entry_maphong.insert(0, str(self.maphong))
        self.entry_loaiphong.insert(0, str(self.loaiphong))
        self.entry_giaphong.insert(0, str(self.giaphong))
        self.entry_tienphong.insert(0, str(self.tongtienphong))
        self.entry_tiendv.insert(0, str(self.tongtiendv))
        self.entry_tong.insert(0, str(self.thanhtien))
        self.ngaynhan.set_date(self.ngaynhan_dt)
        self.ngaytra.set_date(self.ngaytra_dt)

        self.entry_tenkh.config(state = "disabled")
        self.entry_maphong.config(state = "disabled")
        self.entry_loaiphong.config(state = "disabled")
        self.entry_giaphong.config(state = "disabled")
        self.entry_tienphong.config(state = "disabled")
        self.entry_tiendv.config(state = "disabled")
        self.entry_tong.config(state = "disabled")

    # ============================= Thông tin phòng =============================
    def HienThiThongTinDV(self):
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.execute('''SELECT dv.MaDV, dv.TenDV, ctdv.SoLuong, dv.GiaDV, ctdv.SoLuong * dv.GiaDV AS ThanhTien
                          FROM ChiTietDichVu ctdv
                          JOIN DichVu dv ON ctdv.MaDV = dv.MaDV
                          WHERE ctdv.MaDatPhong = ?''', (self.madp,))
        rows = cursor.fetchall()

        # Xóa dữ liệu cũ trong Treeview
        for item in self.ctdv.get_children():
            self.ctdv.delete(item)

        # Hiển thị dữ liệu mới
        for row in rows:
            clean_row = [str(col).replace("(", "").replace(")", "").replace("'", "") for col in row]
            self.ctdv.insert("", "end", values = clean_row)
        conn.close()

    # ================== ĐÓNG FORM ==================
    def on_close(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn thoát không?"):
            self.destroy()
            
    # =============================================== GIAO DIỆN ===============================================
    # =========================================================================================================
    def TaoGiaoDien(self):

        # ==== TIÊU ĐỀ =====
        self.title_label = tk.Label(
            self,
            text="HOÁ ĐƠN",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="black"
        )
        self.title_label.place(x=350, y=10, anchor="n")

        tk.Label(self, text="Ngày……tháng……năm……",
                 font=("Arial", 10), bg="white").place(x=530, y=15)

        # ==== THÔNG TIN KHÁCH HÀNG ====
        tk.Label(self, text="Tên khách hàng", font=("Arial", 10),
                 bg="white").place(x=40, y=70)
        self.entry_tenkh = tk.Entry(self, font=("Arial", 10))
        self.entry_tenkh.place(x=150, y=70, width=170)

        tk.Label(self, text="Mã phòng", font=("Arial", 10),
                 bg="white").place(x=40, y=100)
        self.entry_maphong = tk.Entry(self, font=("Arial", 10))
        self.entry_maphong.place(x=150, y=100, width=170)

        tk.Label(self, text="Loại phòng", font=("Arial", 10),
                 bg="white").place(x=40, y=130)
        self.entry_loaiphong = tk.Entry(self, font=("Arial", 10))
        self.entry_loaiphong.place(x=150, y=130, width=170)

        tk.Label(self, text="Giá phòng", font=("Arial", 10),
                 bg="white").place(x=40, y=160)
        self.entry_giaphong = tk.Entry(self, font=("Arial", 10))
        self.entry_giaphong.place(x=150, y=160, width=170)

        # ==== NGÀY ====
        tk.Label(self, text="Ngày nhận", font=("Arial", 10),
                 bg="white").place(x=380, y=70)
        self.ngaynhan = DateEntry(self, date_pattern="dd/MM/yyyy")
        self.ngaynhan.place(x=470, y=70, width=150)

        tk.Label(self, text="Ngày trả", font=("Arial", 10),
                 bg="white").place(x=380, y=100)
        self.ngaytra = DateEntry(self, date_pattern="dd/MM/yyyy")
        self.ngaytra.place(x=470, y=100, width=150)

        # ==== TIỀN ====
        tk.Label(self, text="Tiền phòng", font=("Arial", 10),
                 bg="white").place(x=40, y=365)
        self.entry_tienphong = tk.Entry(self, font=("Arial", 10))
        self.entry_tienphong.place(x=110, y=365, width=100)

        tk.Label(self, text="Tiền dịch vụ", font=("Arial", 10),
                 bg="white").place(x=230, y=365)
        self.entry_tiendv = tk.Entry(self, font=("Arial", 10))
        self.entry_tiendv.place(x=310, y=365, width=100)

        tk.Label(self, text="Tổng", font=("Arial", 10),
                 bg="white").place(x=430, y=365)
        self.entry_tong = tk.Entry(self, font=("Arial", 10))
        self.entry_tong.place(x=470, y=365, width=100)

        # ==== CHỮ KÝ ====
        tk.Label(self, text="Người lập", font=("Arial", 10),
                 bg="white").place(x=150, y=430)
        tk.Label(self, text="Khách hàng", font=("Arial", 10),
                 bg="white").place(x=500, y=430)
        
        # === BẢNG THÔNG TIN DỊCH VỤ ===
        tk.Label(self, text="Dịch vụ đã sử dụng", font=("Arial", 10), bg="white").place(x=40, y=200)

        frame_ctdv = tk.Frame(self, bg="white")
        frame_ctdv.place(x=10, y=230, width=720, height=120)  # đặt frame nhỏ hơn và không chồng lên Entry

        self.ctdv = ttk.Treeview(frame_ctdv,
                                     columns=("MaDV", "TenDV", "SoLuong", "GiaDV", "ThanhTien"),
                                     show="headings")

        scroll_y = tk.Scrollbar(frame_ctdv, orient="vertical", command=self.ctdv.yview)
        scroll_x = tk.Scrollbar(frame_ctdv, orient="horizontal", command=self.ctdv.xview)
        self.ctdv.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.ctdv.pack(fill="both", expand=True)

        self.ctdv.heading("MaDV", text="Mã dịch vụ")
        self.ctdv.heading("TenDV", text="Tên dịch vụ")
        self.ctdv.heading("SoLuong", text="Số lượng")
        self.ctdv.heading("GiaDV", text="Giá dịch vụ")
        self.ctdv.heading("ThanhTien", text="Thành tiền")

        self.ctdv.column("MaDV", width=80)
        self.ctdv.column("TenDV", width=200)
        self.ctdv.column("SoLuong", width=80)
        self.ctdv.column("GiaDV", width=100)
        self.ctdv.column("ThanhTien", width=120)