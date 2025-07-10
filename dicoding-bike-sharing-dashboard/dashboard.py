import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Bike Sharing Dashboard', layout='wide')
st.title("📊 Bike Sharing Analysis Dashboard")
st.markdown("Dashboard interaktif ini menyajikan analisis penyewaan sepeda berdasarkan data harian dan per jam selama tahun 2011–2012.")

# Load Data
# @st.cache_data
def load_data():
    df_day = pd.read_csv('day.csv')
    df_hour = pd.read_csv('hour.csv')
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    return df_day, df_hour

df_day, df_hour = load_data()

# Clustering (df_day)
df_day['cnt_cluster'] = pd.cut(df_day['cnt'], bins=[0, 2000, 4000, 6000, 9000], labels=['Sepi', 'Sedang', 'Ramai', 'Sangat Ramai'])
df_day['zona_suhu'] = pd.cut(df_day['temp'], bins=[0, 0.3, 0.6, 1.0], labels=['Dingin', 'Sejuk', 'Panas'])
df_day['resiko_cuaca'] = np.where((df_day['hum'] > 0.75) | (df_day['windspeed'] > 0.25), 'Cuaca Buruk', 'Cuaca Baik')
df_day['dominasi_pengguna'] = np.where(df_day['casual'] > df_day['registered'], 'Casual', 'Registered')
df_day['jenis_hari'] = df_day.apply(lambda row: 'Libur' if row['holiday'] == 1 else ('Akhir Pekan' if row['weekday'] in [0,6] else 'Hari Kerja'), axis=1)

# Clustering (df_hour)
df_hour['cnt_cluster'] = pd.cut(df_hour['cnt'], bins=[0, 100, 200, 400, 1000], labels=['Sepi', 'Sedang', 'Ramai', 'Sangat Ramai'])
df_hour['zona_suhu'] = pd.cut(df_hour['temp'], bins=[0, 0.3, 0.6, 1.0], labels=['Dingin', 'Sejuk', 'Panas'])
df_hour['resiko_cuaca'] = np.where((df_hour['hum'] > 0.75) | (df_hour['windspeed'] > 0.25), 'Cuaca Buruk', 'Cuaca Baik')
df_hour['dominasi_pengguna'] = np.where(df_hour['casual'] > df_hour['registered'], 'Casual', 'Registered')
df_hour['jenis_hari'] = df_hour.apply(lambda row: 'Libur' if row['holiday'] == 1 else ('Akhir Pekan' if row['weekday'] in [0,6] else 'Hari Kerja'), axis=1)
df_hour['jenis_jam'] = pd.cut(df_hour['hr'], bins=[-1, 5, 10, 15, 20, 23], labels=['Dini Hari', 'Pagi', 'Siang', 'Sore', 'Malam'])

# Sidebar filter
st.sidebar.header("🔎 Filter Data")

tahun_option = st.sidebar.multiselect(
    "Pilih Tahun", 
    ['2011', '2012'], 
    default=['2011', '2012']
)

musim_option = st.sidebar.multiselect(
    "Pilih Musim", 
    ['1 (Spring)', '2 (Summer)', '3 (Fall)', '4 (Winter)'], 
    default=['1 (Spring)', '2 (Summer)', '3 (Fall)', '4 (Winter)']
)

selected_years = [0 if year == '2011' else 1 for year in tahun_option]
selected_seasons = [int(m[0]) for m in musim_option]

# Filter dataset
df_day_filtered = df_day[df_day['yr'].isin(selected_years) & df_day['season'].isin(selected_seasons)]
df_hour_filtered = df_hour[df_hour['yr'].isin(selected_years) & df_hour['season'].isin(selected_seasons)]

# Download Data  
st.sidebar.markdown("### ⬇️ Unduh Data yang Sudah Diolah")
st.sidebar.download_button(
    label="Download df_day (CSV)", 
    data=df_day.to_csv(index=False),
    file_name="df_day_clustering.csv",
    mime="text/csv"
)
st.sidebar.download_button(
    label="Download df_hour (CSV)", 
    data=df_hour.to_csv(index=False),
    file_name="df_hour_clustering.csv",
    mime="text/csv"
)

st.sidebar.markdown("### ⬇️ Download Raw Data")
st.sidebar.download_button("Download df_day (CSV)", df_day.to_csv(index=False), "df_day.csv", "text/csv")
st.sidebar.download_button("Download df_hour (CSV)", df_hour.to_csv(index=False), "df_hour.csv", "text/csv")

# Tabs untuk pertanyaan bisnis 
tabs = st.tabs([
    "1. Perbandingan Tahun",
    "2. Pola Bulanan",
    "3. Musiman",
    "4. Suhu & Cuaca",
    "5. Pola 24 Jam",
    "6. Hari Tertinggi",
    "7. Lonjakan Tidak Biasa",
    "8. Perilaku Pengguna",
    "9. Pertumbuhan Pengguna"
])

# Tab 1: Perbandingan Tahun
with tabs[0]:
    st.subheader("📅 Perbandingan Jumlah Penyewaan antara 2011 dan 2012")
    fig, ax = plt.subplots()
    sns.barplot(x='yr', y='cnt', data=df_day_filtered, ci=None, ax=ax)
    ax.set_xticklabels(['2011', '2012'])
    ax.set_title("Total Penyewaan per Tahun (Terfilter)")
    st.pyplot(fig)

# Tab 2: Pola Bulanan
with tabs[1]:
    st.subheader("📆 Pola Penyewaan Bulanan")
    monthly = df_day_filtered.groupby(['yr', 'mnth'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    for yr, label in zip([0, 1], ['2011', '2012']):
        subset = monthly[monthly['yr'] == yr]
        ax.plot(subset['mnth'], subset['cnt'], label=label)
    ax.set_xticks(range(1, 13))
    ax.set_title("Pola Bulanan Penyewaan Sepeda (Terfilter)")
    ax.legend()
    st.pyplot(fig)

# Tab 3: Perbandingan Musim
with tabs[2]:
    st.subheader("⛅ Rata-rata Penyewaan per Musim")
    fig, ax = plt.subplots()
    sns.barplot(x='season', y='cnt', data=df_day_filtered, ci=None, ax=ax)
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

# Tab 4: Suhu & Cuaca
with tabs[3]:
    st.subheader("🌡️ Pengaruh Suhu, Kelembaban, dan Cuaca")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.scatterplot(x='temp', y='cnt', data=df_day_filtered, ax=ax[0])
    ax[0].set_title("Suhu vs Penyewaan")
    sns.boxplot(x='weathersit', y='cnt', data=df_day_filtered, ax=ax[1])
    ax[1].set_title("Cuaca vs Penyewaan")
    st.pyplot(fig)

# Tab 5: Pola 24 Jam
with tabs[4]:
    st.subheader("🕓 Rata-rata Penggunaan Sepeda 24 Jam")
    by_hour = df_hour_filtered.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(x='hr', y='cnt', data=by_hour, ax=ax)
    ax.set_title("Penyewaan Rata-rata per Jam (Terfilter)")
    st.pyplot(fig)

# Tab 6: Hari Tertinggi
with tabs[5]:
    st.subheader("📅 Hari dengan Jumlah Penyewaan Tertinggi")
    df_day_filtered['day_name'] = df_day_filtered['dteday'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    fig, ax = plt.subplots()
    sns.barplot(x='day_name', y='cnt', data=df_day_filtered, order=weekday_order, ax=ax)
    ax.set_title("Penyewaan Rata-rata per Hari (Terfilter)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

# Tab 7: Lonjakan Tidak Biasa
with tabs[6]:
    st.subheader("⚠️ Lonjakan Tidak Biasa")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_day_filtered['dteday'], df_day_filtered['cnt'], color='tab:red')
    ax.set_title("Total Penyewaan Harian (Terfilter)")
    st.pyplot(fig)

# Tab 8: Perilaku Pengguna
with tabs[7]:
    st.subheader("👥 Perbedaan Perilaku Pengguna")
    by_hour_user = df_hour_filtered.groupby('hr')[['casual', 'registered']].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(by_hour_user['hr'], by_hour_user['casual'], label='Casual', color='orange')
    ax.plot(by_hour_user['hr'], by_hour_user['registered'], label='Registered', color='blue')
    ax.set_title("Casual vs Registered (Terfilter)")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.legend()
    st.pyplot(fig)

# Tab 9: Pertumbuhan Pengguna 
with tabs[8]:
    st.subheader("📈 Pertumbuhan Pengguna 2011 vs 2012 (Terpisah)")
    
    yearly = df_day_filtered.groupby('yr')[['casual', 'registered']].sum().reset_index()
    yearly['yr'] = yearly['yr'].map({0: '2011', 1: '2012'})

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    sns.barplot(x='yr', y='casual', data=yearly, ax=ax[0], color='orange')
    ax[0].set_title("Casual")
    ax[0].set_ylabel("Total Penyewaan")

    sns.barplot(x='yr', y='registered', data=yearly, ax=ax[1], color='blue')
    ax[1].set_title("Registered")
    ax[1].set_ylabel("Total Penyewaan")

    st.pyplot(fig)

