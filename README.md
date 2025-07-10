# 📊 Dicoding Bike Sharing Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis data penyewaan sepeda selama tahun 2011–2012.

## ✨ Fitur Analisis

- Perbandingan jumlah penyewaan antara tahun 2011 dan 2012
- Pola bulanan dan musiman penyewaan sepeda
- Pengaruh suhu, kelembaban, angin, dan cuaca terhadap penyewaan
- Rata-rata penggunaan sepeda dalam 24 jam
- Perbedaan perilaku pengguna **casual** dan **registered**
- Klasterisasi (`cnt_cluster`, `zona_suhu`, `jenis_hari`, dll)
- Filter interaktif: tahun dan musim
- Download hasil analisis dalam CSV

---

## 🚀 Cara Menjalankan Aplikasi

### 🔧 1. Setup Environment dengan Anaconda

```bash
conda create --name bike-ds python=3.9
conda activate bike-ds
pip install -r requirements.txt
```

### 🐚 2. Setup Environment dengan Shell / Terminal

```bash
mkdir "Dicoding Bike Sharing"
cd "Dicoding Bike Sharing"
pipenv install
pipenv shell
pip install -r requirements.txt
```

###  ▶️ 3. Jalankan Aplikasi Streamlit

```bash
streamlit run dashboard.py
```
