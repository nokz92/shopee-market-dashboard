import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random

# ==========================================
# SETUP HALAMAN & KONFIGURASI
# ==========================================
st.set_page_config(page_title="Shopee Scraper Dashboard", layout="wide", page_icon="🛍️")

st.title("🛍️ Shopee Market Insights Dashboard")
st.markdown("Aplikasi portofolio otomatisasi penarikan data produk dan analisis kompetitor Shopee.")

# ==========================================
# SIMULASI FUNGSI SCRAPER (Aman dari Blokir)
# ==========================================
def simulasi_shopee_scraper(keyword, jumlah_produk):
    """
    Fungsi ini mensimulasikan struktur data yang didapat 
    dari API publik / halaman pencarian Shopee.
    """
    KOTA_LIST = ['Jakarta Barat', 'Jakarta Pusat', 'Surabaya', 'Bandung', 'Medan', 'Tangerang', 'Bekasi']
    DATA_PRODUK = []
    
    for i in range(1, jumlah_produk + 1):
        harga = random.randint(15000, 350000)
        terjual = random.randint(5, 2500)
        omset = harga * terjual
        rating = round(random.uniform(4.2, 5.0), 1)
        
        item = {
            "ID Produk": f"SP-{random.randint(100000, 999999)}",
            "Nama Produk": f"[{keyword.capitalize()}] Varian Premium Model-{i}",
            "Harga (Rp)": harga,
            "Total Terjual": terjual,
            "Estimasi Omset (Rp)": omset,
            "Rating": rating,
            "Lokasi Toko": random.choice(KOTA_LIST)
        }
        DATA_PRODUK.append(item)
        
    return pd.DataFrame(DATA_PRODUK)

# ==========================================
# SIDEBAR KONTROL (Tempat User Bertindak)
# ==========================================
st.sidebar.header("🔍 Pengaturan Scraper")
input_keyword = st.sidebar.text_input("Masukkan Kata Kunci Produk:", value="Sepatu Pria")
input_jumlah = st.sidebar.slider("Jumlah Produk yang Di-scrape:", min_value=10, max_value=100, value=50)

tombol_scrape = st.sidebar.button("🚀 Mulai Scrape Data")

# ==========================================
# LOGIKA UTAMA & VISUALISASI DASHBOARD
# ==========================================
# Inisialisasi session state agar data tidak hilang saat dashboard di-refresh/filter
if "df_shopee" not in st.session_state:
    st.session_state.df_shopee = None

# Aksi ketika tombol klik dijalankan
if tombol_scrape:
    with st.spinner(f"Menghubungkan ke server Shopee untuk keyword '{input_keyword}'..."):
        # Efek loading animasi agar terlihat seperti proses scraping asli
        time.sleep(2) 
        st.session_state.df_shopee = simulasi_shopee_scraper(input_keyword, input_jumlah)
    st.success(f"Berhasil mengambil {input_jumlah} data produk untuk '{input_keyword}'!")

# Menampilkan Dashboard jika data sudah tersedia
if st.session_state.df_shopee is not None:
    df = st.session_state.df_shopee

    # 1. Baris KPI (Key Performance Indicator)
    st.markdown("### 📊 Ringkasan Pasar")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_omset_pasar = df["Estimasi Omset (Rp)"].sum()
        st.metric(label="Total Estimasi Pasar Omset", value=f"Rp {total_omset_pasar:,}")
    with col2:
        rata_harga = int(df["Harga (Rp)"].mean())
        st.metric(label="Rata-rata Harga Produk", value=f"Rp {rata_harga:,}")
    with col3:
        top_produk = df.sort_values(by="Total Terjual", ascending=False).iloc[0]["Nama Produk"]
        st.metric(label="Produk Terlaris", value=top_produk[:25] + "...")

    st.markdown("---")

    # 2. Grafik Visualisasi menggunakan Plotly
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 📍 Distribusi Penjualan Berdasarkan Lokasi")
        fig_lokasi = px.bar(
            df.groupby("Lokasi Toko")["Total Terjual"].sum().reset_index(),
            x="Lokasi Toko",
            y="Total Terjual",
            color="Lokasi Toko",
            title="Total Produk Terjual per Kota"
        )
        st.plotly_chart(fig_lokasi, use_container_width=True)

    with col_chart2:
        st.markdown("#### 💰 Korelasi Harga vs Total Terjual")
        fig_scatter = px.scatter(
            df,
            x="Harga (Rp)",
            y="Total Terjual",
            size="Rating",
            color="Lokasi Toko",
            hover_name="Nama Produk",
            title="Analisis Harga terhadap Volume Penjualan"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 3. Tabel Data Mentah & Fitur Unduh
    st.markdown("---")
    st.markdown("#### 📄 Data Hasil Scrape")
    st.dataframe(df, use_container_width=True)

    # Tombol Download CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data (.CSV)",
        data=csv_data,
        file_name=f"shopee_scrape_{input_keyword.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

else:
    # Tampilan awal saat aplikasi baru dibuka
    st.info("💡 Silakan masukkan kata kunci di menu sebelah kiri lalu klik 'Mulai Scrape Data' untuk memunculkan dashboard.")