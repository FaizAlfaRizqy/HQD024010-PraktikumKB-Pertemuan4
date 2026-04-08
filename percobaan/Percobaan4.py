import tkinter as tk
from tkinter import messagebox

# DATA PENYAKIT & GEJALA
#Struktur : "Nama Penyakit" : ["Gejala1", "Gejala2", ...]
database_penyakit = {
    "Malaria Tertiana": ["nyeri_otot", "muntah", "kejang"],
    "Malaria Quartana": ["menggigil", "tidak_enak_badan", "nyeri_otot"],
    "Malaria Tropika": ["keringat_dingin", "sakit_kepala", "mimisan", "mual"],
    "Malaria Pernisiosa": ["menggigil", "tidak_enak_badan", "demam", "mimisan", "mual"]
}

# DAFTAR SEMUA GEJALA UNTUK PERTANYAAN
semua_gejala = [
    ("nyeri_otot", "Apakah Anda merasa nyeri otot?"),
    ("muntah", "Apakah Anda muntah-muntah?"),
    ("kejang", "Apakah Anda mengalami kejang-kejang?"),
    ("menggigil", "Apakah Anda sering menggigil?"),
    ("tidak_enak_badan", "Apakah Anda merasa tidak enak badan?"),
    ("demam", "Apakah Anda mengalami demam?"),
    ("keringat_dingin", "Apakah Anda sering keringat dingin?"),
    ("sakit_kepala", "Apakah Anda merasa sakit kepala?"),
    ("mimisan", "Apakah Anda mengalami mimisan?"),
    ("mual", "Apakah Anda merasa mual?")
]

class AplikasiPakar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pakar Diagnosa Malaria")
        self.gejala_terpilih = []
        self.index_pertanyaan = 0
    
        # Label Pertanyaan
        self.label_tanya = tk.Label(root, text="Selamat Datang di Sistem Pakar", font=("Arial", 12))
        self.label_tanya.pack(pady=20)
    
        # Tombol Mulai
        self.btn_mulai = tk.Button(root, text="Mulai Diagnosa", command=self.mulai_tanya)
        self.btn_mulai.pack(pady=10)
    
        # Frame Tombol Jawaban (Disembunyikan di awal)
        self.frame_jawaban = tk.Frame(root)
        self.btn_ya = tk.Button(self.frame_jawaban, text="YA", width=10, command=lambda: self.jawab('y'))
        self.btn_tidak = tk.Button(self.frame_jawaban, text="TIDAK", width=10, command=lambda: self.jawab('t'))
        self.btn_ya.pack(side=tk.LEFT, padx=10)
        self.btn_tidak.pack(side=tk.LEFT, padx=10)

    def mulai_tanya(self):
        self.gejala_terpilih = []
        self.index_pertanyaan = 0
        self.btn_mulai.pack_forget()  # Sembunyikan tombol mulai
        self.frame_jawaban.pack(pady=20) 
        self.tampilkan_pertanyaan()

    def tampilkan_pertanyaan(self):
        if self.index_pertanyaan < len(semua_gejala):
            kode, teks = semua_gejala[self.index_pertanyaan]
            self.label_tanya.config(text=teks)
        else:
            self.proses_hasil()

    def jawab(self, respon):
        if respon == 'y':
            kode = semua_gejala[self.index_pertanyaan][0]
            self.gejala_terpilih.append(kode)
        self.index_pertanyaan += 1
        self.tampilkan_pertanyaan()

    def proses_hasil(self):
        hasil = []
        for penyakit, syarat in database_penyakit.items():
            # Cek apakah semua gejala_terpilih mengandung semua syarat untuk penyakit tersebut
            if all(s in self.gejala_terpilih for s in syarat):
                hasil.append(penyakit)

        kesimpulan = ", ".join(hasil) if hasil else "Tidak terdeteksi penyakit"
        messagebox.showinfo("Hasil Diagnosa", f"Berdasarkan gejala Anda:\n\n{kesimpulan}")

        # Reset ke awal
        self.frame_jawaban.pack_forget()
        self.btn_mulai.pack(pady=10)
        self.label_tanya.config(text="Diagnosis Selesai. Ingin mengulang?")

# Menjalankan Aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x250")
    app = AplikasiPakar(root)
    root.mainloop()