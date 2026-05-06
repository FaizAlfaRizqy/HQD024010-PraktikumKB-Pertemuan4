"""
Sistem Pakar Diagnosa Kerusakan Komputer (Console)

Fungsi utama: `diagnose(symptoms: list[str]) -> dict`

Program menyediakan knowledge base sederhana menggunakan dictionary,
mesin inferensi berbasis pencocokan gejala, dan antarmuka console.
"""
from typing import List, Dict, Set, Tuple


# Knowledge base: setiap kerusakan memetakan ke sekumpulan gejala dan solusi singkat
KNOWLEDGE_BASE: Dict[str, Dict[str, object]] = {
    "RAM Rusak": {
        "symptoms": {
            "Sering blue screen (BSOD)",
            "Komputer restart sendiri",
            "Beep saat boot",
            "Aplikasi crash tiba-tiba",
        },
        "solution": "Coba pasang ulang modul RAM, bersihkan pin dengan penghapus karet, atau ganti modul RAM."
    },
    "PSU Lemah": {
        "symptoms": {
            "Komputer tidak nyala sama sekali",
            "Hanya lampu indikator menyala",
            "Restart saat beban tinggi",
            "Tidak ada arus ke komponen lain",
        },
        "solution": "Periksa kabel power, ganti PSU jika tegangan tidak stabil atau lemah."
    },
    "Overheat (Prosesor)": {
        "symptoms": {
            "Komputer mendadak mati tanpa pesan",
            "Kipas CPU berputar kencang terus",
            "Angka suhu CPU tinggi",
            "Kinerja menurun saat beban berat",
        },
        "solution": "Bersihkan kipas dan heatsink, ganti thermal paste, pastikan aliran udara casing baik."
    },
    "VGA Bermasalah": {
        "symptoms": {
            "Layar gelap tetapi komputer menyala",
            "Artefak grafis atau garis pada layar",
            "Driver crash atau reset",
            "Blue screen saat main game",
        },
        "solution": "Perbarui driver VGA, periksa koneksi kabel, atau coba kartu VGA di komputer lain."
    },
    "Hardisk Corrupt": {
        "symptoms": {
            "Sistem lambat saat baca/tulis disk",
            "Bunyi ketukan dari HDD",
            "File tidak bisa dibuka atau corrupt",
            "Gagal boot dengan pesan file system error",
        },
        "solution": "Backup data segera, jalankan chkdsk atau gunakan tool pemulihan; ganti HDD jika ada suara mekanis."
    },
}


def aggregate_symptoms(kb: Dict[str, Dict[str, object]]) -> List[str]:
    seen: List[str] = []
    for info in kb.values():
        for s in info["symptoms"]:
            if s not in seen:
                seen.append(s)
    return seen


SYMPTOMS: List[str] = aggregate_symptoms(KNOWLEDGE_BASE)


def diagnose(input_symptoms: List[str]) -> Dict[str, object]:
    """
    Diagnosa berdasarkan daftar gejala (list of symptom strings).

    Mengembalikan dict berisi: name (str)|solution (str)|score (float)|matched (set)
    Jika tidak ada kecocokan yang cukup, `name` akan bernilai None.
    """
    user_set: Set[str] = set(s.strip() for s in input_symptoms if s and s.strip())
    best: Tuple[str, float, Set[str]] = (None, 0.0, set())

    for disease, info in KNOWLEDGE_BASE.items():
        disease_symptoms: Set[str] = set(info["symptoms"])
        matched = user_set & disease_symptoms
        if not matched:
            continue
        score = len(matched) / len(disease_symptoms)
        if score > best[1] or (score == best[1] and len(matched) > len(best[2])):
            best = (disease, score, matched)

    if best[0] is None or best[1] < 0.5:
        return {
            "name": None,
            "solution": None,
            "score": best[1],
            "matched": set(),
        }

    return {
        "name": best[0],
        "solution": KNOWLEDGE_BASE[best[0]]["solution"],
        "score": round(best[1], 2),
        "matched": best[2],
    }


def _print_interactive():
    print("Sistem Pakar Diagnosa Kerusakan Komputer\n")
    print("Pilih gejala yang dialami (masukkan nomor dipisah koma):\n")
    for i, s in enumerate(SYMPTOMS, start=1):
        print(f"{i}. {s}")

    raw = input("\nMasukkan nomor gejala (misal: 1,3,5): ")
    try:
        nums = [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        print("Input tidak valid. Gunakan nomor dipisahkan koma.")
        return

    chosen = [SYMPTOMS[n - 1] for n in nums if 1 <= n <= len(SYMPTOMS)]
    if not chosen:
        print("Tidak ada gejala terpilih.")
        return

    result = diagnose(chosen)
    if result["name"] is None:
        print("\nHasil: Gejala tidak cocok dengan kerusakan yang diketahui.")
        print("Saran: Coba konsultasi teknisi atau berikan detail gejala lebih lanjut.")
    else:
        print(f"\nDiagnosa: {result['name']}")
        print(f"Solusi singkat: {result['solution']}")
        print(f"Kecocokan gejala: {result['score'] * 100:.0f}%")


import tkinter as tk
from tkinter import messagebox


# Knowledge base: kode penyakit -> list gejala (kode)
DATABASE = {
    "RAM Rusak": {
        "symptoms": ["bsod", "restart", "beep", "app_crash"],
        "solution": "Pasang ulang RAM, bersihkan pin dengan penghapus, atau ganti modul RAM."
    },
    "PSU Lemah": {
        "symptoms": ["no_power", "led_only", "restart_load", "no_power_to_components"],
        "solution": "Periksa kabel power dan tegangan; ganti PSU jika diperlukan."
    },
    "Overheat (Prosesor)": {
        "symptoms": ["random_shutdown", "fan_fast", "high_temp", "slow_under_load"],
        "solution": "Bersihkan heatsink/kipas, ganti thermal paste, perbaiki aliran udara."
    },
    "VGA Bermasalah": {
        "symptoms": ["black_screen", "artifacts", "driver_crash", "bsod_game"],
        "solution": "Perbarui driver, cek kabel, atau uji kartu VGA di komputer lain."
    },
    "Hardisk Corrupt": {
        "symptoms": ["slow_io", "hdd_noise", "file_corrupt", "boot_error"],
        "solution": "Backup data, jalankan chkdsk/utility recovery; ganti HDD/SSD jika rusak."
    }
}


# Semua gejala: (kode, teks pertanyaan)
SEMUA_GEJALA = [
    ("bsod", "Sering blue screen (BSOD)?"),
    ("restart", "Komputer restart sendiri?"),
    ("beep", "Ada bunyi beep saat boot?"),
    ("app_crash", "Aplikasi sering crash tiba-tiba?"),
    ("no_power", "Komputer tidak nyala sama sekali?"),
    ("led_only", "Hanya lampu indikator menyala tanpa POST?"),
    ("restart_load", "Restart saat beban berat (game/compile)?"),
    ("no_power_to_components", "Beberapa komponen tidak mendapatkan daya?") ,
    ("random_shutdown", "Komputer mati mendadak tanpa peringatan?"),
    ("fan_fast", "Kipas CPU berputar kencang terus?"),
    ("high_temp", "Terdapat suhu CPU/GPU sangat tinggi?"),
    ("slow_under_load", "Kinerja menurun saat beban berat?"),
    ("black_screen", "Layar gelap tetapi komputer menyala?"),
    ("artifacts", "Muncul artefak grafis atau garis pada layar?"),
    ("driver_crash", "Driver grafis sering crash/reset?"),
    ("bsod_game", "Blue screen khusus saat menjalankan game?"),
    ("slow_io", "Sistem lambat saat baca/tulis disk?"),
    ("hdd_noise", "Terdengar bunyi ketukan dari HDD?"),
    ("file_corrupt", "Banyak file corrupt atau tidak bisa dibuka?"),
    ("boot_error", "Gagal boot dengan pesan file system error?")
]


def diagnose(selected_codes: list) -> dict:
    """Return best matching disease (or None) and solution."""
    sel = set(selected_codes)
    best = (None, 0.0)
    for disease, info in DATABASE.items():
        syms = set(info["symptoms"])
        matched = sel & syms
        if not matched:
            continue
        score = len(matched) / len(syms)
        if score > best[1]:
            best = (disease, score)

    if best[0] is None or best[1] < 0.5:
        return {"name": None, "score": best[1], "solution": None}

    return {"name": best[0], "score": round(best[1], 2), "solution": DATABASE[best[0]]["solution"]}


class AplikasiPakar:
    def __init__(self, root):
        self.root = root
        root.title("Sistem Pakar Diagnosa Komputer")
        self.index = 0
        self.selected = []

        self.label = tk.Label(root, text="Selamat datang — Tekan Mulai untuk diagnosa", font=(None, 12))
        self.label.pack(pady=12)

        self.btn_start = tk.Button(root, text="Mulai Diagnosa", command=self.start)
        self.btn_start.pack(pady=6)

        self.frame_btn = tk.Frame(root)
        self.btn_yes = tk.Button(self.frame_btn, text="YA", width=10, command=lambda: self.answer(True))
        self.btn_no = tk.Button(self.frame_btn, text="TIDAK", width=10, command=lambda: self.answer(False))
        self.btn_yes.pack(side=tk.LEFT, padx=8)
        self.btn_no.pack(side=tk.LEFT, padx=8)

    def start(self):
        self.selected = []
        self.index = 0
        self.btn_start.pack_forget()
        self.frame_btn.pack(pady=10)
        self.show_question()

    def show_question(self):
        if self.index < len(SEMUA_GEJALA):
            code, text = SEMUA_GEJALA[self.index]
            self.label.config(text=text)
        else:
            self.show_result()

    def answer(self, yes: bool):
        code = SEMUA_GEJALA[self.index][0]
        if yes:
            self.selected.append(code)
        self.index += 1
        self.show_question()

    def show_result(self):
        res = diagnose(self.selected)
        if res["name"] is None:
            msg = "Gejala tidak cocok dengan kerusakan yang diketahui."
        else:
            msg = f"Diagnosa: {res['name']}\nSolusi: {res['solution']}\nKecocokan: {res['score']*100:.0f}%"

        messagebox.showinfo("Hasil Diagnosa", msg)
        self.frame_btn.pack_forget()
        self.btn_start.pack(pady=6)
        self.label.config(text="Diagnosis selesai. Ingin mengulang?")


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('420x220')
    app = AplikasiPakar(root)
    root.mainloop()
