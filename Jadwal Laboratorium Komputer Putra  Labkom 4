import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="Booking Lab Komputer 4 IBM", page_icon="💻", layout="wide")

# ===== PASSWORD ADMIN UNTUK HAPUS =====
PASSWORD_ADMIN = "admin123"

st.markdown("""
<style>
  .header { background:linear-gradient(135deg,#667eea,#764ba2); color:white; padding:25px; border-radius:15px; text-align:center; }
  .libur { background:#ffe0e0; color:red; font-weight:bold; text-align:center; padding:10px; border-radius:10px; }
  .kosong { background:#d4edda; color:#155724; padding:5px 10px; border-radius:20px; font-weight:bold; font-size:12px; }
  .terisi { background:#f8d7da; color:#721c24; padding:5px 10px; border-radius:20px; font-weight:bold; font-size:12px; }
</style>
<div class="header"><h1>💻 JADWAL BOOKING LAB KOMPUTER 4 IBM</h1><p>SMA PUTRA • DESEMBER 2026 • JUMAT LIBUR • MINGGU MASUK</p><p>Link ini untuk Guru - Silakan Booking Disini</p></div>
""", unsafe_allow_html=True)

JAM_LIST = [
    ("Jam ke-1", "07.00 - 07.40"), ("Jam ke-2", "07.40 - 08.20"),
    ("Jam ke-3", "08.20 - 09.00"), ("Jam ke-4", "09.00 - 09.40"),
    ("Jam ke-5", "10.10 - 10.50"), ("Jam ke-6", "10.50 - 11.30"),
    ("Jam ke-7", "11.30 - 12.10"), ("Jam ke-8", "13.40 - 14.20"),
    ("Jam ke-9", "14.20 - 15.00"),
]
HARI_ID = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]

# ===== 1. JADWAL KOSONG DI AWAL =====
if "booking" not in st.session_state:
    st.session_state.booking = []

# ===== FORM BOOKING =====
st.markdown("### 📝 FORM BOOKING - GURU ISI DI SINI")
with st.form("form_booking", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        tanggal = st.selectbox("📅 Tanggal", list(range(1, 32)), format_func=lambda x: f"{x} Desember 2026 - {HARI_ID[datetime.date(2026,12,x).weekday()]}")
        hari = HARI_ID[datetime.date(2026,12,tanggal).weekday()]
        kelas = st.text_input("🏫 Kelas", placeholder="Contoh: X-1")
    with c2:
        jam_pilih = st.selectbox("🕐 Jam Ke", [j[0] for j in JAM_LIST])
        waktu = dict(JAM_LIST)[jam_pilih]
        pelajaran = st.text_input("📚 Pelajaran", placeholder="Contoh: Informatika")
    with c3:
        guru = st.text_input("👨‍🏫 Nama Guru", placeholder="Contoh: Bpk. Ahmad")
        materi = st.text_input("📝 Materi", placeholder="Contoh: Microsoft Word")
    
    if hari == "Jumat":
        st.markdown('<div class="libur">🕌 HARI JUMAT LIBUR - TIDAK BISA BOOKING</div>', unsafe_allow_html=True)
    
    tombol = st.form_submit_button("✅ SIMPAN BOOKING", use_container_width=True)
    if tombol:
        if hari == "Jumat":
            st.error("Maaf, Hari Jumat Libur!")
        elif not kelas or not guru or not pelajaran:
            st.warning("⚠️ Kelas, Pelajaran, dan Guru wajib diisi!")
        else:
            bentrok = [b for b in st.session_state.booking if b["Tanggal"]==tanggal and b["Jam"]==jam_pilih]
            if bentrok:
                st.error(f"❌ SUDAH DIBOOKING! Tanggal {tanggal} {jam_pilih} sudah dipakai kelas {bentrok[0]['Kelas']} oleh {bentrok[0]['Guru']}. Pilih jam lain.")
            else:
                st.session_state.booking.append({"Tanggal": tanggal, "Hari": hari, "Jam": jam_pilih, "Waktu": waktu, "Kelas": kelas, "Pelajaran": pelajaran, "Guru": guru, "Materi": materi})
                st.success(f"✅ Berhasil! {kelas} - {pelajaran} tanggal {tanggal} Desember {jam_pilih} sudah dibooking.")
                st.rerun()  # ===== OTOMATIS UPDATE =====

st.markdown("---")

# ===== TABEL JADWAL =====
st.markdown("### 📋 JADWAL YANG SUDAH DIBOOKING")
cari = st.text_input("🔍 Cari Kelas / Guru / Pelajaran...", "")

if len(st.session_state.booking) == 0:
    st.info("📭 Jadwal masih KOSONG. Belum ada yang booking. Silakan isi form di atas.")
else:
    df = pd.DataFrame(st.session_state.booking).sort_values(["Tanggal", "Jam"])
    if cari:
        df = df[df.apply(lambda r: cari.lower() in str(r.values).lower(), axis=1)]
    
    if len(df) > 0:
        df_tampil = df.copy()
        df_tampil["Tanggal"] = df_tampil["Tanggal"].apply(lambda x: f"{x} Desember 2026")
        # Tambah kolom Status
        df_tampil["Status"] = "✅ TERISI"
        st.dataframe(df_tampil[["Tanggal","Hari","Jam","Waktu","Kelas","Pelajaran","Guru","Materi","Status"]], use_container_width=True, hide_index=True)
        st.markdown(f"**Total Booking:** {len(df)} jadwal")
    else:
        st.info("Tidak ditemukan.")

st.markdown("---")

# ===== 3. HAPUS OLEH ADMIN (PEMBATALAN) =====
st.markdown("### 🔐 HAPUS BOOKING - KHUSUS ADMIN (PEMBATALAN)")
st.caption("Hanya admin yang tahu password yang bisa menghapus. Guru tidak bisa menghapus.")

if len(st.session_state.booking) == 0:
    st.write("Tidak ada jadwal untuk dihapus.")
else:
    # Buat pilihan untuk dihapus
    pilihan_list = []
    for i, b in enumerate(st.session_state.booking):
        pilihan_list.append(f"{b['Tanggal']} Des - {b['Jam']} - {b['Kelas']} - {b['Pelajaran']} - {b['Guru']}")
    
    c_hapus1, c_hapus2, c_hapus3 = st.columns([3, 2, 1])
    with c_hapus1:
        pilih_hapus = st.selectbox("Pilih jadwal yang mau dibatalkan:", pilihan_list)
    with c_hapus2:
        pw = st.text_input("Password Admin", type="password", placeholder="Masukkan password admin")
    with c_hapus3:
        st.write("")  # spacer
        st.write("")
        tombol_hapus = st.button("🗑️ HAPUS", type="primary")
    
    if tombol_hapus:
        if pw != PASSWORD_ADMIN:
            st.error("❌ Password salah! Hanya admin yang bisa menghapus.")
        else:
            idx = pilihan_list.index(pilih_hapus)
            hapus_data = st.session_state.booking.pop(idx)
            st.success(f"✅ Berhasil dibatalkan: {hapus_data['Kelas']} tanggal {hapus_data['Tanggal']} {hapus_data['Jam']}")
            st.rerun()

    # Hapus Semua (Admin juga)
    with st.expander("⚠️ Hapus Semua Jadwal (Reset)"):
        pw2 = st.text_input("Password Admin untuk Hapus Semua", type="password", key="pw2")
        if st.button("🗑️ HAPUS SEMUA"):
            if pw2 == PASSWORD_ADMIN:
                st.session_state.booking = []
                st.success("Semua jadwal sudah dihapus.")
                st.rerun()
            else:
                st.error("Password salah!")

st.markdown("<p style='text-align:center; color:grey; font-size:12px; margin-top:20px;'>Lab Komputer 4 IBM SMA Putra • Desember 2026 • Password Admin saat ini: admin123 - Nanti Bapak bisa ganti di kode</p>", unsafe_allow_html=True)
