import streamlit as st
import requests
import pandas as pd

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzZ9zC9H3W9E4mB2iZ5x6f4bPq1l0gVjU8yT9zNk3qWvE7aLQ/exec"
PASSWORD_ADMIN = "admin123"

st.set_page_config(page_title="Booking Lab Komputer 4", layout="wide")
st.markdown("<h1 style='text-align:center'>JADWAL BOOKING LAB KOMPUTER 4</h1>", unsafe_allow_html=True)

JADWAL = {
    "Senin": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00", "12.30 - 13.10", "13.10 - 13.50", "13.50 - 14.30", "14.30 - 15.10"],
    "Selasa": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00", "12.30 - 13.10", "13.10 - 13.50", "13.50 - 14.30", "14.30 - 15.10"],
    "Rabu": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00", "12.30 - 13.10", "13.10 - 13.50", "13.50 - 14.30", "14.30 - 15.10"],
    "Kamis": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00", "12.30 - 13.10", "13.10 - 13.50", "13.50 - 14.30", "14.30 - 15.10"],
    "Jumat": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00", "12.30 - 13.10", "13.10 - 13.50", "13.50 - 14.30", "14.30 - 15.10"],
    "Sabtu": ["07.00 - 07.40", "07.40 - 08.20", "08.20 - 09.00", "09.00 - 09.40", "10.00 - 10.40", "10.40 - 11.20", "11.20 - 12.00"],
}

def load_data():
    try:
        r = requests.get(SCRIPT_URL, timeout=10)
        data = r.json()
        if isinstance(data, list):
            return data
        return []
    except:
        return []

def save_data(nama, kelas, mapel, hari, jam, tanggal):
    payload = {"nama": nama, "kelas": kelas, "mapel": mapel, "hari": hari, "jam": jam, "tanggal": tanggal}
    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return True
    except:
        return False

# --- FORM BOOKING ---
st.subheader("Form Booking")
with st.form("form_booking", clear_on_submit=True):
    nama = st.text_input("Nama Guru / Pelajaran", placeholder="Contoh: Pak Budi / Matematika")
    kelas = st.selectbox("Kelas", ["X-1","X-2","X-3","X-4","X-5","XI-1","XI-2","XI-3","XI-4","XII-1","XII-2","XII-3"])
    mapel = st.text_input("Mata Pelajaran", placeholder="Contoh: Informatika")
    hari = st.selectbox("Hari", list(JADWAL.keys()))
    jam = st.selectbox("Jam ke", JADWAL[hari])
    tanggal = st.date_input("Tanggal")
    tombol = st.form_submit_button("SIMPAN BOOKING")

    if tombol:
        if not nama or not mapel:
            st.error("Nama dan Mapel wajib diisi!")
        else:
            ok = save_data(nama, kelas, mapel, hari, jam, str(tanggal))
            if ok:
                st.success("Berhasil tersimpan ke Google Sheet!")
                st.rerun()
            else:
                st.error("Gagal simpan, cek koneksi!")

# --- TAMPILKAN JADWAL ---
st.markdown("---")
st.subheader("JADWAL BOOKING")
data = load_data()
if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada booking. Silakan isi form di atas.")

# --- ADMIN HAPUS ---
st.markdown("---")
st.subheader("ADMIN - Hapus Booking")
pw = st.text_input("Password Admin", type="password")
if st.button("Hapus Semua"):
    if pw != PASSWORD_ADMIN:
        st.error("Password salah!")
    else:
        try:
            requests.post(SCRIPT_URL, json={"action": "clear"}, timeout=10)
            st.success("Semua booking dihapus!")
            st.rerun()
        except:
            st.error("Gagal hapus")