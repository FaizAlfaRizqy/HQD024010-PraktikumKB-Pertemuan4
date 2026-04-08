# DATABASE: Penyakit dan daftar gejalanya [cite: 160]
rules_penyakit = {
    "Malaria Tertiana": {"nyeri_otot", "muntah", "kejang"},
    "Malaria Quartana": {"menggigil", "tidak_enak_badan", "nyeri_otot"},
    "Malaria Tropika": {"keringat_dingin", "sakit_kepala", "mimisan", "mual"},
    "Malaria Pernisiosa": {"menggigil", "tidak_enak_badan", "demam", "mimisan", "mual"}
}

def diagnosa_malaria(gejala_input):
    hasil_diagnosa = []

    for penyakit, gejala_syarat in rules_penyakit.items():
        # Cek apakah SEMUA gejala syarat terpenuhi oleh input user [cite: 175]
        if gejala_syarat.issubset(gejala_input):
            hasil_diagnosa.append(penyakit)

    return hasil_diagnosa if hasil_diagnosa else ["Tidak terdeteksi penyakit"]

# Simulasi seperti perintah assertz di Prolog
gejala_pasien = {"nyeri_otot", "menggigil", "tidak_enak_badan"}
print(f"Hasil Diagnosa: {diagnosa_malaria(gejala_pasien)}")