import flet as ft
import math
import numpy as np # WAJIB: Untuk perhitungan matriks Radius 3P

def main(page: ft.Page):
    page.title = "Surveyor Mate V5 (Master Edition)"
    page.theme_mode = "light"
    page.window_width = 390
    page.window_height = 844
    page.padding = 10
    page.scroll = "auto"

    # --- HELPER FUNCTIONS ---
    def dms_str(deg_decimal):
        """Ubah Desimal ke Derajat Menit Detik"""
        d = int(deg_decimal)
        m = int((deg_decimal - d) * 60)
        s = round(((deg_decimal - d) * 60 - m) * 60, 2)
        return f"{d}° {m}' {s}\""

    # =========================================
    # 1. LOGIKA INVERSE (Jarak & Azimuth)
    # =========================================
    inv_x1 = ft.TextField(label="X Awal (E)", width=150, height=40, text_size=13, keyboard_type="number")
    inv_y1 = ft.TextField(label="Y Awal (N)", width=150, height=40, text_size=13, keyboard_type="number")
    inv_x2 = ft.TextField(label="X Tujuan (E)", width=150, height=40, text_size=13, keyboard_type="number")
    inv_y2 = ft.TextField(label="Y Tujuan (N)", width=150, height=40, text_size=13, keyboard_type="number")
    res_inv_dist = ft.Text("-", weight="bold", size=16)
    res_inv_az = ft.Text("-", weight="bold", size=16, color="blue")

    def calc_inverse(e):
        try:
            x1, y1 = float(inv_x1.value), float(inv_y1.value)
            x2, y2 = float(inv_x2.value), float(inv_y2.value)
            dx = x2 - x1
            dy = y2 - y1
            dist = math.sqrt(dx**2 + dy**2)
            az_rad = math.atan2(dx, dy)
            az_deg = math.degrees(az_rad)
            if az_deg < 0: az_deg += 360
            
            res_inv_dist.value = f"Jarak: {dist:.3f} m"
            res_inv_az.value = f"Azimuth: {dms_str(az_deg)}"
            page.update()
        except:
            res_inv_dist.value = "Error Input!"
            page.update()
            
    # =========================================
    # 2. LOGIKA POLARA (Cari Koord Baru)
    # =========================================
    pol_x1 = ft.TextField(label="X Alat", width=150, height=40, text_size=13, keyboard_type="number")
    pol_y1 = ft.TextField(label="Y Alat", width=150, height=40, text_size=13, keyboard_type="number")
    pol_az = ft.TextField(label="Azimuth (°)", width=150, height=40, text_size=13, keyboard_type="number")
    pol_dist = ft.TextField(label="Jarak Datar", width=150, height=40, text_size=13, keyboard_type="number")
    res_pol_x = ft.Text("X: -", weight="bold", color="green")
    res_pol_y = ft.Text("Y: -", weight="bold", color="green")

    def calc_polara(e):
        try:
            x1, y1 = float(pol_x1.value), float(pol_y1.value)
            az = float(pol_az.value)
            d = float(pol_dist.value)
            az_rad = math.radians(az)
            x2 = x1 + d * math.sin(az_rad)
            y2 = y1 + d * math.cos(az_rad)
            res_pol_x.value = f"X Baru: {x2:.3f}"
            res_pol_y.value = f"Y Baru: {y2:.3f}"
            page.update()
        except:
            res_pol_x.value = "Cek Angka!"
            page.update()

    # =========================================
    # 3. LOGIKA INTERPOLASI ELEVASI
    # =========================================
    int_z1 = ft.TextField(label="Z Awal", width=100, height=40, text_size=13, keyboard_type="number")
    int_z2 = ft.TextField(label="Z Akhir", width=100, height=40, text_size=13, keyboard_type="number")
    int_dt = ft.TextField(label="Jarak Total", width=100, height=40, text_size=13, keyboard_type="number")
    int_dx = ft.TextField(label="Jarak X", width=100, height=40, text_size=13, keyboard_type="number")
    res_int_z = ft.Text("-", size=20, weight="bold", color="purple")
    res_beda_t = ft.Text("-", size=12, italic=True)

    def calc_interp(e):
        try:
            z1, z2 = float(int_z1.value), float(int_z2.value)
            dt, dx = float(int_dt.value), float(int_dx.value)
            beda = z2 - z1
            z_new = z1 + (beda * (dx/dt))
            gradien = (beda / dt) * 100
            res_int_z.value = f"Z Baru: {z_new:.3f}"
            res_beda_t.value = f"Beda: {beda:.3f} m ({gradien:.2f}%)"
            page.update()
        except:
            res_int_z.value = "Error"
            page.update()

    # =========================================
    # 4. LOGIKA SUPERELEVASI
    # =========================================
    sup_z = ft.TextField(label="Z Center", width=150, height=40, text_size=13, keyboard_type="number")
    sup_w = ft.TextField(label="Lebar (m)", width=150, height=40, text_size=13, keyboard_type="number")
    sup_e = ft.TextField(label="Kemiringan (%)", width=150, height=40, text_size=13, keyboard_type="number")
    res_sup = ft.Text("-", size=20, weight="bold", color="red")
    
    def calc_super(e):
        try:
            z_cl = float(sup_z.value)
            w = float(sup_w.value)
            slope = float(sup_e.value)
            delta = w * (slope / 100)
            z_edge = z_cl + delta
            res_sup.value = f"Z Tepi: {z_edge:.3f}"
            page.update()
        except:
            res_sup.value = "Error"
            page.update()
    
    # =========================================
    # 5. LOGIKA MASTER TOOLS (RADIUS & RESECTION)
    # =========================================
    
    # --- FITUR A: RADIUS DARI 3 TITIK (P1, P2, P3) ---
    rad_x1 = ft.TextField(label="X P1", width=100, height=40, text_size=13, keyboard_type="number")
    rad_y1 = ft.TextField(label="Y P1", width=100, height=40, text_size=13, keyboard_type="number")
    rad_x2 = ft.TextField(label="X P2", width=100, height=40, text_size=13, keyboard_type="number")
    rad_y2 = ft.TextField(label="Y P2", width=100, height=40, text_size=13, keyboard_type="number")
    rad_x3 = ft.TextField(label="X P3", width=100, height=40, text_size=13, keyboard_type="number")
    rad_y3 = ft.TextField(label="Y P3", width=100, height=40, text_size=13, keyboard_type="number")

    res_rad_xc = ft.Text("-", size=16)
    res_rad_yc = ft.Text("-", size=16)
    res_rad_r = ft.Text("-", weight="bold", size=20, color="purple")

    def calc_radius_3p(e):
        """Menghitung Center (Xc, Yc) dan Radius (R) dari 3 titik menggunakan sistem persamaan linear."""
        try:
            x1, y1 = float(rad_x1.value), float(rad_y1.value)
            x2, y2 = float(rad_x2.value), float(rad_y2.value)
            x3, y3 = float(rad_x3.value), float(rad_y3.value)
            
            # Persamaan Linear 2x2 untuk mencari Xc dan Yc
            A1 = 2 * (x2 - x1)
            B1 = 2 * (y2 - y1)
            C1 = (x2**2 + y2**2) - (x1**2 + y1**2)

            A2 = 2 * (x3 - x2)
            B2 = 2 * (y3 - y2)
            C2 = (x3**2 + y3**2) - (x2**2 + y2**2)

            D = A1 * B2 - A2 * B1 # Determinan
            Dx = C1 * B2 - C2 * B1 
            Dy = A1 * C2 - A2 * B1
            
            if D == 0:
                 res_rad_r.value = "Error: Titik segaris!"
                 return page.update()

            Xc = Dx / D
            Yc = Dy / D
            
            R = math.sqrt((x1 - Xc)**2 + (y1 - Yc)**2)

            res_rad_xc.value = f"Xc: {Xc:.3f}"
            res_rad_yc.value = f"Yc: {Yc:.3f}"
            res_rad_r.value = f"R: {R:.3f} m"
            page.update()
            
        except Exception as e:
            res_rad_r.value = f"Error: Cek input"
            page.update()
            
    # --- FITUR B: RESECTION (Framework Sederhana) ---
    res_xa = ft.TextField(label="XA", width=100, height=40, text_size=13, keyboard_type="number")
    res_ya = ft.TextField(label="YA", width=100, height=40, text_size=13, keyboard_type="number")
    res_xb = ft.TextField(label="XB", width=100, height=40, text_size=13, keyboard_type="number")
    res_yb = ft.TextField(label="YB", width=100, height=40, text_size=13, keyboard_type="number")
    res_sudut_a = ft.TextField(label="Sudut Alpha (°)", width=150, height=40, text_size=13, keyboard_type="number")
    res_sudut_b = ft.TextField(label="Sudut Beta (°)", width=150, height=40, text_size=13, keyboard_type="number")

    res_resection_xp = ft.Text("XP: -", weight="bold", size=18, color="darkred")
    res_resection_yp = ft.Text("YP: -", weight="bold", size=18, color="darkred")
    
    def calc_resection(e):
        res_resection_xp.value = "XP: [Rumus Master Lanjutan]"
        res_resection_yp.value = "YP: [Butuh Pengembangan Lebih Lanjut]"
        page.update()

    # --- LAYOUT UTAMA ---
    
    page.add(
        ft.Text("SURVEYOR MATE", size=24, weight="bold", text_align="center"),
        ft.Text("Konstruksi Tool (Final Version)", size=12, italic=True, text_align="center"),
        ft.Divider(),
        ft.ListView([
            # Bagian Kalkulator Dasar
            ft.ExpansionTile(
                title=ft.Text("Geometri Dasar"),
                leading=ft.Icon("my_location"),
                initially_expanded=True,
                controls=[
                    ft.Container(padding=10, content=ft.Column([
                        ft.Text("Inverse (Jarak & Azimuth)", weight="bold"),
                        ft.Row([inv_x1, inv_y1], alignment="center"),
                        ft.Row([inv_x2, inv_y2], alignment="center"),
                        ft.ElevatedButton("HITUNG", on_click=calc_inverse, bgcolor="blue", color="white"),
                        ft.Column([res_inv_dist, res_inv_az], horizontal_alignment="center"),
                        ft.Divider(),
                        ft.Text("Polara (Koordinat Baru)", weight="bold"),
                        ft.Row([pol_x1, pol_y1], alignment="center"),
                        ft.Row([pol_az, pol_dist], alignment="center"),
                        ft.ElevatedButton("HITUNG", on_click=calc_polara, bgcolor="green", color="white"),
                        ft.Column([res_pol_x, res_pol_y], horizontal_alignment="center"),
                    ]))
                ]
            ),

            ft.ExpansionTile(
                title=ft.Text("Vertikal"),
                leading=ft.Icon("terrain"),
                controls=[
                    ft.Container(padding=10, content=ft.Column([
                        ft.Text("Interpolasi Elevasi", weight="bold"),
                        ft.Row([int_z1, int_z2], alignment="center"),
                        ft.Row([int_dt, int_dx], alignment="center"),
                        ft.ElevatedButton("HITUNG INTERP", on_click=calc_interp, width=320, bgcolor="purple", color="white"),
                        res_int_z, res_beda_t
                    ], horizontal_alignment="center"))
                ]
            ),
            
            ft.ExpansionTile(
                title=ft.Text("Jalan Raya"),
                leading=ft.Icon("add_road"),
                controls=[
                    ft.Container(padding=10, content=ft.Column([
                        ft.Text("Superelevasi (Cek Tepi)", weight="bold"),
                        ft.Row([sup_z, sup_w], alignment="center"),
                        sup_e,
                        ft.ElevatedButton("HITUNG Z TEPI", on_click=calc_super, width=320, bgcolor="orange", color="white"),
                        res_sup
                    ], horizontal_alignment="center"))
                ]
            ),

            # Bagian Kalkulator Lanjutan (Master Tools)
            ft.ExpansionTile(
                title=ft.Text("MASTER TOOLS (Kurva & Resection)", weight="bold"),
                leading=ft.Icon("stars"),
                controls=[
                    ft.Container(padding=10, content=ft.Column([
                        ft.Text("Radius Kurva (3 Titik)", weight="bold"),
                        ft.Row([rad_x1, rad_y1], alignment="center"),
                        ft.Row([rad_x2, rad_y2], alignment="center"),
                        ft.Row([rad_x3, rad_y3], alignment="center"),
                        ft.ElevatedButton("HITUNG RADIUS", on_click=calc_radius_3p, width=320, bgcolor="purple", color="white"),
                        ft.Column([res_rad_xc, res_rad_yc, res_rad_r], horizontal_alignment="center"),
                        
                        ft.Divider(),

                        ft.Text("Resection (Penentuan Titik Alat)", weight="bold"),
                        ft.Row([res_xa, res_ya], alignment="center"),
                        ft.Row([res_xb, res_yb], alignment="center"),
                        ft.Row([res_sudut_a, res_sudut_b], alignment="center"),
                        ft.Text("*Input 3 Titik Kontrol (A, B, C) dan Sudut di P.", size=10, italic=True),
                        ft.ElevatedButton("HITUNG RESECTION", on_click=calc_resection, width=320, bgcolor="red", color="white"),
                        ft.Column([res_resection_xp, res_resection_yp], horizontal_alignment="center")
                    ]))
                ]
            ),
        ], expand=True, spacing=10)
    )

ft.app(target=main)