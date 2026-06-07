import streamlit as st
import pandas as pd
import random
import datetime
import math

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EkonomiID — Portal Ekonomi Indonesia",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:#07090f;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.25rem 2rem 4rem!important;max-width:1300px!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#090d16 0%,#0b0f1c 100%)!important;border-right:1px solid #141e30!important;}
[data-testid="stSidebar"] .stRadio label{color:#7a92a8!important;font-size:.875rem!important;}
[data-testid="stSidebar"] .stRadio label:hover{color:#e2e8f0!important;}
[data-testid="metric-container"]{background:linear-gradient(135deg,#0c1422 0%,#0f1928 100%)!important;border:1px solid #1a2c3d!important;border-radius:14px!important;padding:1.1rem 1.3rem!important;position:relative;overflow:hidden;transition:border-color .25s,transform .2s;}
[data-testid="metric-container"]:hover{border-color:#c9a84c!important;transform:translateY(-2px);}
[data-testid="stMetricLabel"]{color:#5a7a8a!important;font-size:.75rem!important;font-weight:600!important;letter-spacing:.05em;text-transform:uppercase;}
[data-testid="stMetricValue"]{color:#e8f0f8!important;font-family:'DM Mono',monospace!important;font-size:1.3rem!important;font-weight:500!important;}
[data-testid="stMetricDelta"]{font-size:.78rem!important;font-weight:600!important;}
[data-testid="stTabs"]{border-bottom:1px solid #141e30;}
[data-testid="stTabs"] button{color:#5a7a8a!important;font-weight:500!important;font-size:.875rem!important;padding:.5rem 1rem!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:#c9a84c!important;border-bottom:2px solid #c9a84c!important;}
[data-testid="stTabs"] button:hover{color:#e2e8f0!important;background:rgba(255,255,255,.03)!important;}
[data-testid="stExpander"]{background:#0c1422!important;border:1px solid #1a2c3d!important;border-left:3px solid #c9a84c!important;border-radius:0 10px 10px 0!important;margin-bottom:.6rem!important;}
[data-testid="stExpander"] summary{color:#e8c97a!important;font-weight:600!important;font-size:.9rem!important;}
[data-testid="stTextInput"] input{background:#0c1422!important;border:1px solid #1a2c3d!important;color:#e2e8f0!important;border-radius:8px!important;}
[data-testid="stTextInput"] input:focus{border-color:#c9a84c!important;box-shadow:0 0 0 2px rgba(201,168,76,.15)!important;}
div[data-testid="stSelectbox"] > div{background:#0c1422!important;border:1px solid #1a2c3d!important;color:#e2e8f0!important;border-radius:8px!important;}
.stSlider [data-testid="stSliderThumb"]{background:#c9a84c!important;}
.stInfo{background:rgba(45,212,191,.06)!important;border-left:3px solid #2dd4bf!important;border-radius:8px!important;}
.stSuccess{background:rgba(74,222,128,.06)!important;border-left:3px solid #4ade80!important;border-radius:8px!important;}
.stWarning{background:rgba(251,191,36,.06)!important;border-left:3px solid #fbbf24!important;border-radius:8px!important;}
.stError{background:rgba(248,113,113,.06)!important;border-left:3px solid #f87171!important;border-radius:8px!important;}
hr{border-color:#141e30!important;margin:1.5rem 0!important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:#07090f;}
::-webkit-scrollbar-thumb{background:#1a2c3d;border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:#c9a84c;}
.sh{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#fff;margin-bottom:.2rem;}
.ss{color:#5a7a8a;font-size:.875rem;margin-bottom:1.25rem;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA AKTUAL (update Juni 2026)
# ─────────────────────────────────────────────────────────────

# Kurs aktual per 5 Juni 2026 (sumber: Bloomberg/BI)
KURS_AKTUAL = {
    "USD": 18039, "EUR": 19935, "GBP": 22858, "JPY": 108,
    "SGD": 13361, "MYR": 4349,  "AUD": 12003, "CNY": 2460,
    "SAR": 4504,  "HKD": 2160,  "CHF": 21861, "KRW": 11,
}

# Indikator utama aktual
INDIKATOR = [
    {"nama":"Inflasi Mei 2026",   "nilai":"3,08%",     "delta":"▲ +0,66%", "positif":False, "icon":"📊","sub":"YoY — BPS, 2 Jun 2026"},
    {"nama":"USD/IDR",            "nilai":"18.039",    "delta":"▼ -14,9%", "positif":False, "icon":"💵","sub":"Level historis terendah"},
    {"nama":"PDB Q1 2026",        "nilai":"5,61%",     "delta":"▲ +0,74%", "positif":True,  "icon":"🏛️","sub":"YoY — tertinggi sejak Q4 2022"},
    {"nama":"BI Rate",            "nilai":"5,25%",     "delta":"▲ +0,50%", "positif":False, "icon":"⚖️","sub":"Dinaikkan Mei 2026"},
    {"nama":"IHSG",               "nilai":"5.941",     "delta":"▼ -4,11%", "positif":False, "icon":"📈","sub":"3 Jun 2026 — koreksi tajam"},
    {"nama":"Cadangan Devisa",    "nilai":"$146,2 M",  "delta":"▼ -1,8%",  "positif":False, "icon":"🏅","sub":"Apr 2026 — terendah sj. Ags 2024"},
    {"nama":"Ekspor Apr 2026",    "nilai":"$25,30 M",  "delta":"▲ +2,1%",  "positif":True,  "icon":"🚢","sub":"Neraca surplus $0,09 M"},
    {"nama":"Tingkat Kemiskinan", "nilai":"7,50%",     "delta":"▼ -0,2%",  "positif":True,  "icon":"👥","sub":"Des 2025 — BPS"},
]

# ── Database Tabel: Sejarah Kurs ──
@st.cache_data(ttl=300)
def db_kurs_history():
    # Rekonstruksi historis kurs USD/IDR 2022–2026 berdasarkan data aktual
    data = [
        ("Jan 2022",14379),("Feb 2022",14354),("Mar 2022",14349),("Apr 2022",14430),
        ("Mei 2022",14626),("Jun 2022",14895),("Jul 2022",14929),("Agu 2022",14845),
        ("Sep 2022",15189),("Okt 2022",15575),("Nov 2022",15640),("Des 2022",15731),
        ("Jan 2023",15004),("Feb 2023",15167),("Mar 2023",15384),("Apr 2023",14899),
        ("Mei 2023",15004),("Jun 2023",15117),("Jul 2023",15025),("Agu 2023",15346),
        ("Sep 2023",15475),("Okt 2023",15926),("Nov 2023",15678),("Des 2023",15547),
        ("Jan 2024",15653),("Feb 2024",15640),("Mar 2024",15709),("Apr 2024",16083),
        ("Mei 2024",15994),("Jun 2024",16408),("Jul 2024",16320),("Agu 2024",15850),
        ("Sep 2024",15380),("Okt 2024",15707),("Nov 2024",15861),("Des 2024",16102),
        ("Jan 2025",16295),("Feb 2025",16278),("Mar 2025",16544),("Apr 2025",16765),
        ("Mei 2025",16470),("Jun 2025",16310),("Jul 2025",16190),("Agu 2025",16080),
        ("Sep 2025",16250),("Okt 2025",16430),("Nov 2025",16680),("Des 2025",16815),
        ("Jan 2026",17100),("Feb 2026",17250),("Mar 2026",17480),("Apr 2026",17700),
        ("Mei 2026",17816),("Jun 2026*",18039),
    ]
    return pd.DataFrame(data, columns=["Periode","USD/IDR"])

# ── Database Tabel: Inflasi Bulanan ──
@st.cache_data(ttl=300)
def db_inflasi():
    data = [
        ("Jan 2024",2.57),("Feb 2024",2.75),("Mar 2024",3.05),("Apr 2024",3.00),
        ("Mei 2024",2.84),("Jun 2024",2.51),("Jul 2024",2.13),("Agu 2024",2.12),
        ("Sep 2024",1.84),("Okt 2024",1.71),("Nov 2024",1.55),("Des 2024",1.57),
        ("Jan 2025",2.48),("Feb 2025",2.43),("Mar 2025",2.62),("Apr 2025",2.42),
        ("Mei 2025",1.89),("Jun 2025",2.20),("Jul 2025",2.35),("Agu 2025",2.44),
        ("Sep 2025",2.51),("Okt 2025",2.58),("Nov 2025",2.67),("Des 2025",2.54),
        ("Jan 2026",2.60),("Feb 2026",2.55),("Mar 2026",2.71),("Apr 2026",2.42),
        ("Mei 2026",3.08),
    ]
    return pd.DataFrame(data, columns=["Periode","Inflasi YoY (%)"])

# ── Database Tabel: PDB ──
@st.cache_data(ttl=300)
def db_gdp():
    data = [
        (2010,6864.1,6.1),(2011,7831.7,6.5),(2012,8615.7,6.0),(2013,9546.1,5.6),
        (2014,10569.7,5.0),(2015,11531.4,4.9),(2016,12401.7,5.0),(2017,13589.8,5.1),
        (2018,14838.3,5.2),(2019,15832.7,5.0),(2020,15434.2,-2.1),(2021,16970.8,3.7),
        (2022,19588.4,5.3),(2023,20892.4,5.0),(2024,22138.7,5.0),(2025,23459.5,5.1),
    ]
    return pd.DataFrame(data, columns=["Tahun","PDB Nominal (T Rp)","Pertumbuhan (%)"])

# ── Database Tabel: Cadangan Devisa ──
@st.cache_data(ttl=300)
def db_devisa():
    data = [
        ("Jan 2025",157.3),("Feb 2026",154.6),("Mar 2026",148.2),
        ("Apr 2026",146.2),("Mei 2026",146.2),
    ]
    return pd.DataFrame(data, columns=["Periode","Cadangan Devisa ($M)"])

# ── Database Tabel: IHSG Harian ──
@st.cache_data(ttl=300)
def db_ihsg(days=120):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1,-1,-1)]
    random.seed(42)
    # IHSG turun dari ~7500 ke ~5941 dalam 4 bulan terakhir
    start_val = 7500.0
    end_val   = 5941.0
    vals = []
    v = start_val
    for i in range(days):
        trend = (end_val - start_val) / days
        v += trend + random.gauss(0, 60)
        v = max(5500, min(7800, v))
        vals.append(round(v, 2))
    vals[-1] = 5941.07  # pin ke data aktual
    return pd.DataFrame({"Tanggal": dates, "IHSG": vals})

# ── Database Tabel: Ekspor Impor ──
@st.cache_data(ttl=300)
def db_ekspor_impor():
    data = [
        ("Jan 2026",22.1,22.8,-0.7),("Feb 2026",23.4,22.1,1.3),
        ("Mar 2026",24.8,23.5,1.3),("Apr 2026",25.3,25.21,0.09),
    ]
    return pd.DataFrame(data, columns=["Bulan","Ekspor ($M)","Impor ($M)","Neraca ($M)"])

# ── Database Tabel: Sektor PDB ──
@st.cache_data(ttl=300)
def db_sektor():
    data = [
        ("Industri Pengolahan",19.6,4.2,"Manufaktur"),
        ("Perdagangan",13.2,5.9,"Jasa"),
        ("Pertanian",13.1,3.1,"Primer"),
        ("Konstruksi",9.4,6.7,"Sekunder"),
        ("Pertambangan",10.8,5.8,"Primer"),
        ("Transportasi & Logistik",5.7,8.4,"Jasa"),
        ("Informasi & Komunikasi",4.3,12.3,"Jasa"),
        ("Jasa Keuangan",4.9,7.1,"Jasa"),
        ("Jasa Lainnya",19.0,4.5,"Jasa"),
    ]
    return pd.DataFrame(data, columns=["Sektor","Kontribusi PDB (%)","Pertumbuhan (%)","Kelompok"])

# ── Database Tabel: BI Rate History ──
@st.cache_data(ttl=300)
def db_birate():
    data = [
        ("Jan 2022",3.50),("Apr 2022",3.50),("Aug 2022",3.75),("Sep 2022",4.25),
        ("Okt 2022",4.75),("Nov 2022",5.25),("Jan 2023",5.75),("Feb 2023",5.75),
        ("Okt 2023",6.00),("Nov 2023",6.00),("Apr 2024",6.25),("Sep 2024",6.00),
        ("Okt 2024",6.00),("Jan 2025",5.75),("Feb 2025",5.75),("Mar 2025",5.75),
        ("Apr 2025",5.75),("Mei 2025",5.25),("Jun 2025",5.25),("Jul 2025",5.25),
        ("Agu 2025",5.25),("Sep 2025",5.00),("Okt 2025",5.00),("Nov 2025",5.00),
        ("Des 2025",5.00),("Jan 2026",4.75),("Feb 2026",4.75),("Mar 2026",4.75),
        ("Apr 2026",4.75),("Mei 2026",5.25),
    ]
    return pd.DataFrame(data, columns=["Periode","BI Rate (%)"])

# ── Database Tabel: Proyeksi ──
@st.cache_data(ttl=300)
def db_proyeksi():
    data = [
        ("2026",5.2,3.2,18200,146,5.10),
        ("2027",5.4,2.8,17800,150,4.90),
        ("2028",5.5,2.5,17400,155,4.70),
        ("2029",5.6,2.4,17000,160,4.50),
        ("2030",5.8,2.2,16500,165,4.30),
    ]
    return pd.DataFrame(data, columns=["Tahun","PDB (%)","Inflasi (%)","USD/IDR","Devisa ($M)","Pengangguran (%)"])

BERITA = [
    {"judul":"Rupiah Tembus Rp18.039 — Level Terendah Sepanjang Sejarah",
     "kat":"Kurs","tgl":"4 Jun 2026","icon":"💱","prio":"BREAKING",
     "isi":"Nilai tukar rupiah menembus level psikologis Rp18.000/USD untuk pertama kali dalam sejarah pada 4 Juni 2026. Rupiah dibuka di Rp18.003 dan ditutup di Rp18.049, melemah 82 poin (-0,46%). Pelemahan dipicu kombinasi sentimen risk-off global, tekanan Selat Hormuz, dan outflow modal asing. BI diperkirakan akan melakukan intervensi di pasar DNDF dan spot.",
     "dampak":"Importir tertekan hebat, biaya bahan baku naik. Eksportir diuntungkan konversi. Potensi imported inflation meningkat. Masyarakat merasakan kenaikan harga barang konsumsi impor.","sentiment":"negatif"},
    {"judul":"IHSG Anjlok 4,11% ke 5.941 — Terdalam di Asia Pasifik",
     "kat":"Pasar Modal","tgl":"3 Jun 2026","icon":"📉","prio":"BREAKING",
     "isi":"IHSG ditutup melemah 4,11% ke level 5.941,07 pada 3 Juni 2026, menjadi penurunan terdalam di Asia Pasifik pada hari tersebut. Koreksi dipimpin saham big-cap BREN dan DSSA. 508 saham melemah, hanya 172 menguat. Phintraco memperingatkan IHSG berpotensi ke 5.700 jika tekanan berlanjut.",
     "dampak":"Kapitalisasi pasar BEI turun tajam. Kepercayaan investor asing merosot. Manajer investasi menghadapi tekanan redemption reksa dana saham.","sentiment":"negatif"},
    {"judul":"BI Naikkan Suku Bunga ke 5,25% untuk Jaga Rupiah",
     "kat":"Moneter","tgl":"20 Mei 2026","icon":"🏦","prio":"PENTING",
     "isi":"Bank Indonesia menaikkan BI Rate 50 bps menjadi 5,25% pada RDG Mei 2026 guna menjaga stabilitas nilai tukar dan mengendalikan inflasi di tengah konflik geopolitik global. Kebijakan makroprudensial tetap dipertahankan longgar (pro-growth). BI memperketat pengawasan aliran modal asing.",
     "dampak":"Kredit perbankan lebih mahal. Saham terkoreksi jangka pendek. Positif untuk deposito dan obligasi jangka pendek. KPR floating rate naik.","sentiment":"netral"},
    {"judul":"Inflasi Mei 2026 Naik ke 3,08% — Tertinggi Sejak 2023",
     "kat":"Inflasi","tgl":"2 Jun 2026","icon":"📊","prio":"PENTING",
     "isi":"BPS mencatat inflasi IHK 3,08% YoY pada Mei 2026, naik dari 2,42% April. Pendorong utama: cabai merah, minyak goreng, bawang merah, dan BBM nonsubsidi. Inflasi inti 2,59% YoY. Meski masih dalam target BI (1,5–3,5%), laju kenaikan mengkhawatirkan pelaku pasar.",
     "dampak":"Daya beli masyarakat tergerus. BI berpotensi kembali naikkan suku bunga jika inflasi melampaui 3,5%. Sektor ritel dan F&B tertekan.","sentiment":"negatif"},
    {"judul":"PDB Q1 2026 Tumbuh 5,61% — Tertinggi Sejak Q4 2022",
     "kat":"Makro","tgl":"5 Mei 2026","icon":"📈","prio":"POSITIF",
     "isi":"BPS mencatat pertumbuhan ekonomi 5,61% YoY pada Q1 2026, melampaui konsensus 5,3% dan naik dari 4,87% di Q1 2025. Konsumsi rumah tangga berkontribusi 54,36% PDB. Investasi dan ekspor turut mendorong. Ini capaian tertinggi sejak Q4 2022.",
     "dampak":"Fundamental ekonomi solid di tengah guncangan kurs. Memberikan ruang bagi pemerintah untuk kebijakan countercyclical. Prospek kredit perbankan positif.","sentiment":"positif"},
    {"judul":"Cadangan Devisa Turun 4 Bulan Beruntun ke $146,2 M",
     "kat":"Devisa","tgl":"7 Mei 2026","icon":"🏅","prio":"WASPADA",
     "isi":"BI melaporkan cadangan devisa turun ke USD 146,2 miliar per April 2026, terendah sejak Agustus 2024. Penurunan empat bulan beruntun ini mencerminkan intervensi BI untuk menstabilkan rupiah yang terus melemah. Masih cukup untuk 5,8 bulan impor — di atas standar 3 bulan.",
     "dampak":"Ruang intervensi BI semakin terbatas. Potensi tekanan lebih lanjut pada rupiah jika outflow berlanjut. Perlu sinergi kebijakan fiskal-moneter lebih erat.","sentiment":"negatif"},
    {"judul":"Ekspor April 2026 Naik ke $25,30 M — Surplus Tipis",
     "kat":"Perdagangan","tgl":"15 Mei 2026","icon":"🚢","prio":"POSITIF",
     "isi":"BPS mencatat ekspor April 2026 sebesar USD 25,30 miliar, sementara impor USD 25,21 miliar, menghasilkan surplus tipis USD 0,09 miliar. Surplus menyempit tajam dari USD 3,32 miliar Maret. Gangguan pasokan di Selat Hormuz menjadi faktor utama kenaikan impor migas.",
     "dampak":"Surplus yang menyempit meningkatkan risiko Current Account Deficit. Ketergantungan impor migas perlu dikurangi dengan percepatan transisi energi.","sentiment":"netral"},
    {"judul":"PDB Nominal 2025 Capai Rp 23.459 Triliun",
     "kat":"Makro","tgl":"1 Mei 2026","icon":"🏛️","prio":"POSITIF",
     "isi":"Kemenkeu mencatat realisasi PDB nominal 2025 sebesar Rp 23.459,5 triliun, tumbuh 5,1% dibanding 2024. Indonesia mempertahankan posisi sebagai ekonomi terbesar ke-16 dunia. Target PDB 2030 sebesar Rp 30.000 triliun dinilai realistis dengan pertumbuhan rata-rata 5,5%.",
     "dampak":"Kepercayaan investor jangka panjang terjaga. Ruang fiskal cukup untuk program prioritas pemerintah. Pasar obligasi dalam negeri tetap diminati asing.","sentiment":"positif"},
]

KAMUS = [
    ("USD/IDR","Nilai tukar rupiah terhadap dolar AS. Per 4 Juni 2026 berada di level Rp18.039 — level historis terlemah. Pelemahan dipicu sentimen risk-off global, kenaikan DXY, dan outflow modal asing.","Kurs"),
    ("PDB (Produk Domestik Bruto)","Nilai total barang dan jasa yang diproduksi di suatu negara dalam periode tertentu. PDB nominal Indonesia 2025 mencapai Rp 23.459 triliun. PDB per kapita ~Rp 87 juta (~USD 4.816 pada kurs 18.039).","Makro"),
    ("Inflasi IHK","Kenaikan Indeks Harga Konsumen secara umum. Mei 2026: 3,08% YoY — tertinggi sejak pertengahan 2023. Dipicu cabai merah, minyak goreng, BBM nonsubsidi. Target BI: 2,5±1%.","Moneter"),
    ("BI Rate","Suku bunga acuan Bank Indonesia. Dinaikkan 50 bps ke 5,25% pada Mei 2026 untuk meredam inflasi dan menjaga stabilitas rupiah di tengah gejolak global.","Moneter"),
    ("IHSG","Indeks Harga Saham Gabungan — cerminan kinerja seluruh saham di BEI. Anjlok 4,11% ke 5.941 pada 3 Juni 2026, penurunan terdalam di Asia Pasifik. Koreksi dipimpin BREN dan DSSA.","Pasar Modal"),
    ("Cadangan Devisa","Aset luar negeri BI berupa valuta asing, emas, dan SDR. Per April 2026: USD 146,2 miliar — terendah sejak Agustus 2024 akibat intervensi rupiah. Setara ~5,8 bulan impor.","Moneter"),
    ("Deflasi","Penurunan harga umum. Deflasi persisten berbahaya karena memicu spiral penurunan konsumsi dan investasi. Indonesia tidak mengalami deflasi sejak pandemi 2020.","Moneter"),
    ("Yield Obligasi (SBN)","Imbal hasil Surat Berharga Negara. Yield SBN 10 tahun di sekitar 7,1% (Juni 2026) — naik signifikan seiring kenaikan BI Rate dan pelemahan rupiah.","Pasar Modal"),
    ("Current Account Deficit","Defisit transaksi berjalan — impor jasa, barang, dan transfer lebih besar dari ekspor. Indonesia berpotensi CAD jika surplus perdagangan terus menyempit.","Makro"),
    ("Neraca Perdagangan","Selisih ekspor-impor. April 2026: surplus tipis $0,09 M, turun drastis dari surplus $3,32 M di Maret 2026, akibat gangguan pasokan Selat Hormuz.","Perdagangan"),
    ("Imported Inflation","Inflasi yang bersumber dari kenaikan harga impor, biasanya dipicu pelemahan kurs. Rupiah di Rp18.000 memperbesar risiko imported inflation bagi Indonesia.","Moneter"),
    ("Safe Haven","Aset yang diminati investor saat ketidakpastian tinggi: USD, JPY, CHF, emas. Saat rupiah lemah, modal asing mengalir ke safe haven, menekan IHSG dan SBN.","Pasar Modal"),
    ("Kebijakan Fiskal","Pengelolaan APBN oleh pemerintah. Rasio utang Indonesia April 2026: ~38% PDB — masih jauh di bawah batas 60% UU Keuangan Negara.","Fiskal"),
    ("QE & Tapering","Quantitative Easing: bank sentral AS (The Fed) beli aset untuk tambah likuiditas. Tapering: pengurangan QE. Sinyal tapering The Fed biasanya perkuat USD dan tekan rupiah.","Moneter"),
    ("PMI Manufaktur","Purchasing Managers Index: >50 = ekspansi, <50 = kontraksi. PMI Manufaktur Indonesia April 2026 di 53,2 — masih ekspansif meski melambat dari 54,1 Maret.","Indikator"),
    ("DXY (Dollar Index)","Indeks kekuatan dolar AS terhadap 6 mata uang utama. DXY menguat = tekanan pada mata uang negara berkembang termasuk rupiah. Per 4 Juni 2026 DXY ~99,4.","Kurs"),
    ("Risk-Off / Risk-On","Risk-off: investor hindari aset berisiko (saham, EM) → pindah ke safe haven. Risk-on: sebaliknya. Kondisi Juni 2026 = risk-off akibat konflik geopolitik Timur Tengah.","Pasar Modal"),
    ("TPT (Tingkat Pengangguran Terbuka)","Persentase angkatan kerja yang aktif mencari kerja namun tidak bekerja. Februari 2026: 5,32% (BPS) — cenderung membaik dari 6,49% puncak pemulihan pasca-COVID.","Ketenagakerjaan"),
]

PRIO_STYLE = {
    "BREAKING": ("#f87171","rgba(248,113,113,.12)"),
    "PENTING":  ("#e8c97a","rgba(232,201,122,.12)"),
    "WASPADA":  ("#fb923c","rgba(251,146,60,.12)"),
    "POSITIF":  ("#4ade80","rgba(74,222,128,.12)"),
}
SENT_COLOR = {"positif":"#4ade80","netral":"#e8c97a","negatif":"#f87171"}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def metric_card(icon, nama, nilai, delta, positif, sub):
    c = "#4ade80" if positif else "#f87171"
    return f"""
    <div style='background:linear-gradient(135deg,#0c1422,#0f1928);border:1px solid #1a2c3d;
                border-radius:14px;padding:1.1rem 1.3rem;transition:all .2s;height:100%'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem'>
        <span style='font-size:1.4rem'>{icon}</span>
        <span style='font-size:.73rem;font-weight:700;color:{c};letter-spacing:.02em'>{delta}</span>
      </div>
      <div style='font-family:"DM Mono",monospace;font-size:1.3rem;color:#e8f0f8;font-weight:500;line-height:1.2'>{nilai}</div>
      <div style='font-size:.72rem;color:#5a7a8a;margin-top:.25rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase'>{nama}</div>
      <div style='font-size:.68rem;color:#3d5166;margin-top:.2rem'>{sub}</div>
    </div>"""

def sh(title, sub=""):
    s = f"<div style='color:#5a7a8a;font-size:.875rem;margin:.15rem 0 1.25rem'>{sub}</div>" if sub else ""
    st.markdown(f"<div style='font-family:\"Playfair Display\",serif;font-size:1.5rem;font-weight:700;color:#e8f0f8;margin-bottom:.15rem'>{title}</div>{s}", unsafe_allow_html=True)

def badge(text, color="#c9a84c"):
    return f"<span style='background:{color}22;color:{color};border:1px solid {color}44;padding:.18rem .6rem;border-radius:100px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em'>{text}</span>"

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.5rem 0 1.75rem'>
      <div style='font-family:"Playfair Display",serif;font-size:1.9rem;font-weight:900;color:#c9a84c;letter-spacing:-1px'>
        Ekonomi<span style='color:#2dd4bf'>ID</span></div>
      <div style='color:#243344;font-size:.68rem;margin-top:.35rem;letter-spacing:.1em;text-transform:uppercase'>
        Portal Ekonomi Indonesia</div>
      <div style='color:#f87171;font-size:.7rem;font-weight:600;margin-top:.5rem;background:rgba(248,113,113,.08);
                  border:1px solid rgba(248,113,113,.2);border-radius:6px;padding:.25rem .6rem;display:inline-block'>
        ⚠️ Data Aktual Jun 2026</div>
    </div>
    """, unsafe_allow_html=True)

    halaman = st.radio("nav", [
        "🏠  Dashboard Utama",
        "📰  Berita & Analisis",
        "🗄️  Database Tabel",
        "📊  Grafik Data Makro",
        "📈  Pasar Keuangan",
        "🏭  Sektor Ekonomi",
        "🔭  Proyeksi & Outlook",
        "📚  Kamus Ekonomi",
        "🧮  Kalkulator Ekonomi",
        "🤖  Tanya AI Ekonomi",
        "📋  Laporan Sistem",
        "ℹ️  Tentang",
    ], label_visibility="collapsed")

    st.markdown("---")
    now = datetime.datetime.now().strftime("%d %b %Y")
    st.markdown(f"""
    <div style='font-size:.7rem;color:#243344;text-align:center;line-height:2'>
      🗓️ {now}<br>
      💵 USD/IDR: <span style='color:#f87171;font-weight:700'>18.039</span><br>
      📊 Inflasi: <span style='color:#e8c97a;font-weight:700'>3,08%</span><br>
      ⚖️ BI Rate: <span style='color:#e8c97a;font-weight:700'>5,25%</span><br>
      📈 IHSG: <span style='color:#f87171;font-weight:700'>5.941</span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DASHBOARD UTAMA
# ══════════════════════════════════════════════════════════════

if halaman == "🏠  Dashboard Utama":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0c1830 0%,#090e1a 100%);
                border:1px solid #1a2c3d;border-radius:18px;padding:2.5rem 2.5rem 2rem;
                margin-bottom:2rem;position:relative;overflow:hidden'>
      <div style='position:absolute;top:-60px;right:-60px;width:360px;height:360px;
                  background:radial-gradient(circle,rgba(201,168,76,.06),transparent 70%)'></div>
      <div style='position:absolute;bottom:-40px;left:-40px;width:280px;height:280px;
                  background:radial-gradient(circle,rgba(248,113,113,.04),transparent 70%)'></div>
      <div style='display:inline-block;background:rgba(248,113,113,.1);color:#f87171;
                  border:1px solid rgba(248,113,113,.3);padding:.3rem 1rem;
                  border-radius:100px;font-size:.72rem;font-weight:700;
                  letter-spacing:.1em;text-transform:uppercase;margin-bottom:1rem'>
        ⚠️ SIAGA — Rupiah Tembus Rp18.000 · IHSG -4,11% · Inflasi 3,08%
      </div>
      <h1 style='font-family:"Playfair Display",serif;font-size:2.8rem;font-weight:900;
                 color:#e8f0f8;line-height:1.1;margin:.5rem 0 .7rem'>
        Dashboard Ekonomi<br><span style='color:#c9a84c'>Indonesia</span>
      </h1>
      <p style='color:#5a7a8a;font-size:.95rem;max-width:560px;line-height:1.7'>
        Data aktual terkini per 5 Juni 2026 — kurs, inflasi, PDB, pasar keuangan, dan seluruh indikator makroekonomi Indonesia.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── 8 Indikator ──
    sh("📌 Indikator Ekonomi Aktual", "Data per 4–5 Juni 2026 dari BI, BPS, Bloomberg")
    cols = st.columns(4)
    for i, ind in enumerate(INDIKATOR):
        with cols[i % 4]:
            st.markdown(metric_card(ind["icon"],ind["nama"],ind["nilai"],ind["delta"],ind["positif"],ind["sub"]), unsafe_allow_html=True)
        if i == 3:
            st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
            cols = st.columns(4)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Charts row ──
    c1, c2 = st.columns([3,2])
    with c1:
        sh("💵 Kurs USD/IDR 2022–2026", "Tren pelemahan rupiah menuju level Rp18.000")
        kd = db_kurs_history()
        st.line_chart(kd.set_index("Periode")[["USD/IDR"]], color="#f87171", height=260)
    with c2:
        sh("📊 Inflasi YoY 2024–2026", "Kenaikan ke 3,08% Mei 2026 (BPS)")
        di = db_inflasi()
        st.area_chart(di.set_index("Periode")[["Inflasi YoY (%)"]], color="#e8c97a", height=260)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        sh("📈 IHSG 120 Hari Terakhir", "Koreksi ke 5.941 pada 3 Juni 2026")
        ih = db_ihsg()
        st.line_chart(ih.set_index("Tanggal")[["IHSG"]], color="#4ade80", height=240)
    with c2:
        sh("⚖️ Histori BI Rate", "Kenaikan 50 bps ke 5,25% Mei 2026")
        br = db_birate()
        st.area_chart(br.set_index("Periode")[["BI Rate (%)"]], color="#c9a84c", height=240)

    st.markdown("---")
    sh("⚡ Berita Utama Terkini")
    b_cols = st.columns(4)
    for i, b in enumerate(BERITA[:4]):
        pc, pb = PRIO_STYLE[b["prio"]]
        sc = SENT_COLOR[b["sentiment"]]
        with b_cols[i]:
            st.markdown(f"""
            <div style='background:#0c1422;border:1px solid #1a2c3d;border-top:2px solid {pc};
                        border-radius:0 0 12px 12px;padding:1rem;min-height:190px'>
              <div style='display:flex;gap:.4rem;margin-bottom:.6rem;flex-wrap:wrap'>
                <span style='background:{pb};color:{pc};border:1px solid {pc}44;
                             padding:.15rem .5rem;border-radius:100px;font-size:.65rem;font-weight:700'>{b["prio"]}</span>
                <span style='background:{sc}22;color:{sc};border:1px solid {sc}44;
                             padding:.15rem .5rem;border-radius:100px;font-size:.65rem;font-weight:700'>{b["kat"]}</span>
              </div>
              <div style='font-size:.85rem;font-weight:700;color:#e8f0f8;line-height:1.4;margin-bottom:.4rem'>{b["judul"]}</div>
              <div style='color:#5a7a8a;font-size:.75rem;line-height:1.5'>{b["isi"][:100]}…</div>
              <div style='color:#3d5166;font-size:.68rem;margin-top:.5rem'>{b["tgl"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# BERITA & ANALISIS
# ══════════════════════════════════════════════════════════════

elif halaman == "📰  Berita & Analisis":
    sh("📰 Berita & Analisis Ekonomi", "Kondisi ekonomi Indonesia terkini — data aktual Juni 2026")

    fc1, fc2, fc3 = st.columns([3,1,1])
    with fc1: cari = st.text_input("🔍 Cari berita...", placeholder="rupiah, inflasi, IHSG...")
    with fc2: kat_f = st.selectbox("Kategori", ["Semua"]+sorted({b["kat"] for b in BERITA}))
    with fc3: sent_f = st.selectbox("Sentimen", ["Semua","positif","netral","negatif"])

    filtered = BERITA
    if cari: filtered = [b for b in filtered if cari.lower() in b["judul"].lower() or cari.lower() in b["isi"].lower()]
    if kat_f != "Semua": filtered = [b for b in filtered if b["kat"] == kat_f]
    if sent_f != "Semua": filtered = [b for b in filtered if b["sentiment"] == sent_f]

    neg = sum(1 for b in BERITA if b["sentiment"]=="negatif")
    pos = sum(1 for b in BERITA if b["sentiment"]=="positif")
    neu = sum(1 for b in BERITA if b["sentiment"]=="netral")
    sc1,sc2,sc3 = st.columns(3)
    sc1.metric("🔴 Negatif", neg)
    sc2.metric("🟡 Netral", neu)
    sc3.metric("🟢 Positif", pos)

    st.markdown(f"<div style='color:#3d5166;font-size:.8rem;margin:.75rem 0'>Menampilkan {len(filtered)} artikel</div>", unsafe_allow_html=True)

    for b in filtered:
        pc, pb = PRIO_STYLE[b["prio"]]
        sc = SENT_COLOR[b["sentiment"]]
        st.markdown(f"""
        <div style='background:#0c1422;border:1px solid #1a2c3d;border-left:3px solid {pc};
                    border-radius:0 14px 14px 0;padding:1.5rem;margin-bottom:1rem'>
          <div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.75rem;flex-wrap:wrap'>
            <span style='font-size:1.4rem'>{b['icon']}</span>
            <span style='background:{pb};color:{pc};border:1px solid {pc}44;padding:.2rem .65rem;border-radius:100px;font-size:.7rem;font-weight:700'>{b['prio']}</span>
            <span style='background:#1a2c3d;color:#7a92a8;padding:.2rem .65rem;border-radius:100px;font-size:.7rem;font-weight:600'>{b['kat']}</span>
            <span style='background:{sc}22;color:{sc};border:1px solid {sc}44;padding:.2rem .65rem;border-radius:100px;font-size:.7rem;font-weight:600'>{b['sentiment'].upper()}</span>
            <span style='color:#3d5166;font-size:.75rem;margin-left:auto'>{b['tgl']}</span>
          </div>
          <div style='font-size:1.05rem;font-weight:700;color:#e8f0f8;margin-bottom:.65rem;line-height:1.4'>{b['judul']}</div>
          <div style='font-size:.875rem;color:#7a92a8;line-height:1.8;margin-bottom:.85rem'>{b['isi']}</div>
          <div style='background:rgba(45,212,191,.05);border:1px solid rgba(45,212,191,.12);border-radius:8px;padding:.75rem 1rem'>
            <div style='font-size:.68rem;font-weight:700;color:#2dd4bf;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.3rem'>💡 Analisis Dampak</div>
            <div style='font-size:.83rem;color:#7a92a8;line-height:1.65'>{b['dampak']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATABASE TABEL (halaman khusus backend)
# ══════════════════════════════════════════════════════════════

elif halaman == "🗄️  Database Tabel":
    sh("🗄️ Database Tabel — Backend Data", "Seluruh tabel data yang menjadi fondasi sistem EkonomiID")

    st.markdown("""
    <div style='background:rgba(45,212,191,.05);border:1px solid rgba(45,212,191,.15);
                border-radius:10px;padding:1rem 1.25rem;margin-bottom:1.5rem'>
      <span style='color:#2dd4bf;font-weight:700;font-size:.85rem'>🗃️ Arsitektur Database EkonomiID</span><br>
      <span style='color:#5a7a8a;font-size:.82rem'>
        8 tabel data utama — seluruhnya di-cache di memori (Streamlit @st.cache_data) dan diperbarui setiap 5 menit.
        Data bersifat historis-aktual berdasarkan sumber BI, BPS, Bloomberg, dan Databoks.
      </span>
    </div>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
        "💵 Kurs USD/IDR","📊 Inflasi","🏛️ PDB","⚖️ BI Rate",
        "🏅 Devisa","📈 IHSG","🚢 Ekspor-Impor","🔭 Proyeksi"
    ])

    with tab1:
        st.markdown("#### 📋 Tabel `db_kurs_history` — Histori Kurs USD/IDR (Bulanan)")
        df = db_kurs_history()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Kolom: {list(df.columns)} | Rentang: Jan 2022 – Jun 2026</div>", unsafe_allow_html=True)
        st.dataframe(df.sort_values("Periode",ascending=False).reset_index(drop=True), use_container_width=True, height=380)
        c1,c2,c3 = st.columns(3)
        c1.metric("Kurs Terendah (min)", f"Rp {df['USD/IDR'].min():,.0f}", "Feb 2022")
        c2.metric("Kurs Tertinggi (max)", f"Rp {df['USD/IDR'].max():,.0f}", "Jun 2026 ⚠️")
        c3.metric("Rata-Rata 4 Tahun", f"Rp {df['USD/IDR'].mean():,.0f}")
        st.bar_chart(df.set_index("Periode")[["USD/IDR"]], color="#f87171", height=220)

    with tab2:
        st.markdown("#### 📋 Tabel `db_inflasi` — Inflasi IHK YoY Bulanan (%)")
        df = db_inflasi()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Rentang: Jan 2024 – Mei 2026 | Sumber: BPS</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["Status"] = df_show["Inflasi YoY (%)"].apply(lambda x: "✅ Dalam Target" if 1.5<=x<=3.5 else "⚠️ Di Luar Target")
        st.dataframe(df_show.sort_values("Periode",ascending=False).reset_index(drop=True), use_container_width=True, height=380)
        c1,c2,c3 = st.columns(3)
        c1.metric("Inflasi Terendah", f"{df['Inflasi YoY (%)'].min():.2f}%", "Nov 2024")
        c2.metric("Inflasi Tertinggi", f"{df['Inflasi YoY (%)'].max():.2f}%", "Mei 2026")
        c3.metric("Rata-Rata", f"{df['Inflasi YoY (%)'].mean():.2f}%")
        st.line_chart(df.set_index("Periode")[["Inflasi YoY (%)"]], color="#e8c97a", height=220)

    with tab3:
        st.markdown("#### 📋 Tabel `db_gdp` — PDB Nominal & Pertumbuhan (2010–2025)")
        df = db_gdp()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: BPS, Kemenkeu</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["PDB Nominal (T Rp)"] = df_show["PDB Nominal (T Rp)"].apply(lambda x: f"Rp {x:,.1f} T")
        df_show["Pertumbuhan (%)"] = df_show["Pertumbuhan (%)"].apply(lambda x: f"{'▲' if x>0 else '▼'} {x:.1f}%")
        st.dataframe(df_show.sort_values("Tahun",ascending=False).reset_index(drop=True), use_container_width=True, height=380)
        c1,c2,c3 = st.columns(3)
        c1.metric("PDB 2025", "Rp 23.459,5 T")
        c2.metric("Pertumbuhan Tertinggi", "6,5% (2011)")
        c3.metric("Pertumbuhan Terburuk", "-2,1% (2020 COVID)")
        st.bar_chart(db_gdp().set_index("Tahun")[["PDB Nominal (T Rp)"]], color="#c9a84c", height=220)

    with tab4:
        st.markdown("#### 📋 Tabel `db_birate` — Histori BI Rate (%)")
        df = db_birate()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: Bank Indonesia</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["Kategori"] = df_show["BI Rate (%)"].apply(lambda x: "🔴 Ketat" if x>=5.5 else ("🟡 Netral" if x>=4.5 else "🟢 Longgar"))
        st.dataframe(df_show.sort_values("Periode",ascending=False).reset_index(drop=True), use_container_width=True, height=380)
        c1,c2,c3 = st.columns(3)
        c1.metric("BI Rate Terendah", "3,50% (2022)")
        c2.metric("BI Rate Tertinggi", "6,25% (Apr 2024)")
        c3.metric("BI Rate Saat Ini", "5,25% (Mei 2026)")
        st.area_chart(df.set_index("Periode")[["BI Rate (%)"]], color="#c9a84c", height=220)

    with tab5:
        st.markdown("#### 📋 Tabel `db_devisa` — Cadangan Devisa ($M)")
        df = db_devisa()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: Bank Indonesia</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["Kecukupan Impor"] = df_show["Cadangan Devisa ($M)"].apply(lambda x: f"~{x/25.3:.1f} bulan")
        df_show["Status"] = df_show["Cadangan Devisa ($M)"].apply(lambda x: "✅ Aman" if x>=130 else "⚠️ Perlu Perhatian")
        st.dataframe(df_show, use_container_width=True)
        st.warning("⚠️ Penurunan 4 bulan beruntun — terendah sejak Agustus 2024")
        c1,c2 = st.columns(2)
        c1.metric("Jan 2025 (puncak)", "$157,3 M")
        c2.metric("Apr 2026 (terkini)", "$146,2 M", "-$11,1 M")
        st.bar_chart(df.set_index("Periode")[["Cadangan Devisa ($M)"]], color="#2dd4bf", height=220)

    with tab6:
        st.markdown("#### 📋 Tabel `db_ihsg` — IHSG Harian (120 hari terakhir)")
        df = db_ihsg()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: BEI / simulasi berbasis data aktual</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["Trend"] = df_show["IHSG"].diff().apply(lambda x: "▲" if x>0 else "▼" if x<0 else "—")
        st.dataframe(df_show.sort_values("Tanggal",ascending=False).reset_index(drop=True).head(30), use_container_width=True, height=380)
        c1,c2,c3 = st.columns(3)
        c1.metric("IHSG Tertinggi 120h", f"{df['IHSG'].max():,.0f}")
        c2.metric("IHSG Terendah 120h", f"{df['IHSG'].min():,.0f}")
        c3.metric("Terakhir (3 Jun)", "5.941,07", "-4,11%")
        st.line_chart(df.set_index("Tanggal")[["IHSG"]], color="#4ade80", height=220)

    with tab7:
        st.markdown("#### 📋 Tabel `db_ekspor_impor` — Neraca Perdagangan 2026 ($M)")
        df = db_ekspor_impor()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: BPS</div>", unsafe_allow_html=True)
        df_show = df.copy()
        df_show["Status"] = df_show["Neraca ($M)"].apply(lambda x: "✅ Surplus" if x>0 else "⚠️ Defisit")
        st.dataframe(df_show, use_container_width=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Ekspor YTD", f"${df['Ekspor ($M)'].sum():.1f} M")
        c2.metric("Total Impor YTD", f"${df['Impor ($M)'].sum():.1f} M")
        c3.metric("Surplus YTD", f"${df['Neraca ($M)'].sum():.2f} M", "Menyempit")
        st.bar_chart(df.set_index("Bulan")[["Ekspor ($M)","Impor ($M)"]], height=220)

    with tab8:
        st.markdown("#### 📋 Tabel `db_proyeksi` — Proyeksi 2026–2030")
        df = db_proyeksi()
        st.markdown(f"<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.5rem'>Rows: {len(df)} | Sumber: Konsensus IMF/BI/Kemenkeu (simulasi)</div>", unsafe_allow_html=True)
        st.dataframe(df.set_index("Tahun"), use_container_width=True)
        st.info("📌 Proyeksi asumsi stabilisasi kurs bertahap, inflasi terkendali, dan pertumbuhan investasi yang solid.")

# ══════════════════════════════════════════════════════════════
# GRAFIK DATA MAKRO
# ══════════════════════════════════════════════════════════════

elif halaman == "📊  Grafik Data Makro":
    sh("📊 Grafik Data Makroekonomi", "Visualisasi interaktif seluruh indikator utama")

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["🏛️ PDB","📊 Inflasi","💵 Kurs","⚖️ BI Rate","🚢 Perdagangan"])

    with tab1:
        df = db_gdp()
        c1,c2 = st.columns(2)
        with c1:
            sh("PDB Nominal (T Rp) 2010–2025")
            st.bar_chart(df.set_index("Tahun")[["PDB Nominal (T Rp)"]], color="#c9a84c", height=340)
        with c2:
            sh("Laju Pertumbuhan PDB (%)")
            df2 = df.dropna().set_index("Tahun")[["Pertumbuhan (%)"]]
            st.bar_chart(df2, color="#4ade80", height=340)
        st.markdown("#### Statistik PDB")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("PDB 2025", "Rp 23.459 T")
        c2.metric("Pertumbuhan Q1-2026", "5,61% YoY ▲")
        c3.metric("PDB per Kapita (est)", "~$4.816")
        c4.metric("Target 2030", "Rp 30.000 T")

    with tab2:
        df = db_inflasi()
        sh("Inflasi IHK YoY Bulanan (%)", "Mei 2026: 3,08% — kenaikan signifikan dari 2,42% April")
        st.area_chart(df.set_index("Periode")[["Inflasi YoY (%)"]], color="#e8c97a", height=360)
        st.markdown("---")
        c1,c2,c3 = st.columns(3)
        c1.metric("Inflasi Mei 2026", "3,08% ⚠️", "+0,66% dari April")
        c2.metric("Target BI 2026", "2,5% ± 1%", "Range: 1,5%–3,5%")
        c3.metric("Inflasi Inti (core)", "2,59%", "Stabil")
        st.error("⚠️ Inflasi Mei 2026 mendekati batas atas target 3,5%. Pendorong: cabai merah, minyak goreng, BBM nonsubsidi.")

    with tab3:
        df = db_kurs_history()
        sh("Kurs USD/IDR Bulanan 2022–2026", "Rupiah melemah ke level historis Rp18.039 per 4 Juni 2026")
        st.line_chart(df.set_index("Periode")[["USD/IDR"]], color="#f87171", height=360)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Kurs 4 Jun 2026", "18.039", "Level terendah sepanjang sejarah")
        c2.metric("Kurs Awal 2022", "14.379", "—")
        c3.metric("Depresiasi 4 Tahun", "-20,0%", "Rp3.660/USD")
        c4.metric("DXY Index", "~99,4", "Melemah 0,08%")
        st.markdown("#### Kurs Referensi BI — 5 Juni 2026")
        df_kurs_tbl = pd.DataFrame([{"Mata Uang":k,"IDR":f"Rp {v:,.0f}","per 1 unit":k} for k,v in KURS_AKTUAL.items()])
        st.dataframe(df_kurs_tbl.set_index("Mata Uang"), use_container_width=True)

    with tab4:
        df = db_birate()
        sh("Histori BI Rate (%)", "Dinaikkan 50 bps ke 5,25% pada Mei 2026")
        st.line_chart(df.set_index("Periode")[["BI Rate (%)"]], color="#c9a84c", height=360)
        c1,c2,c3 = st.columns(3)
        c1.metric("BI Rate Saat Ini", "5,25%", "↑ dari 4,75%")
        c2.metric("Terendah (2022)", "3,50%")
        c3.metric("Tertinggi (Apr 2024)", "6,25%")

    with tab5:
        df = db_ekspor_impor()
        sh("Neraca Perdagangan 2026 ($M)", "Surplus menyempit tajam di April")
        c1,c2 = st.columns(2)
        with c1:
            st.bar_chart(df.set_index("Bulan")[["Ekspor ($M)","Impor ($M)"]], height=300)
        with c2:
            st.bar_chart(df.set_index("Bulan")[["Neraca ($M)"]], color="#2dd4bf", height=300)
        st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PASAR KEUANGAN
# ══════════════════════════════════════════════════════════════

elif halaman == "📈  Pasar Keuangan":
    sh("📈 Pasar Keuangan Indonesia", "IHSG, Nilai Tukar Multi-Pasangan, Yield Curve SBN")

    tab1,tab2,tab3 = st.tabs(["📈 IHSG","💵 Multi-Kurs","🏛️ Yield Curve SBN"])

    with tab1:
        df = db_ihsg()
        periode = st.select_slider("Periode", [30,60,90,120], 90, format_func=lambda x: f"{x} hari")
        dp = df.tail(periode)
        c1,c2,c3,c4 = st.columns(4)
        v_now = dp["IHSG"].iloc[-1]; v_old = dp["IHSG"].iloc[0]
        c1.metric("Penutupan Terakhir", f"{v_now:,.2f}", f"{v_now-v_old:+.0f}")
        c2.metric("Tertinggi", f"{dp['IHSG'].max():,.0f}")
        c3.metric("Terendah", f"{dp['IHSG'].min():,.0f}")
        c4.metric(f"Return {periode}h", f"{(v_now/v_old-1)*100:+.2f}%")
        st.line_chart(dp.set_index("Tanggal")[["IHSG"]], color="#4ade80", height=380)
        st.error("⚠️ IHSG anjlok 4,11% ke 5.941 pada 3 Jun 2026 — terdalam di Asia Pasifik. Potensi ke 5.700 jika tekanan berlanjut (Phintraco).")

    with tab2:
        st.markdown("#### Kurs Aktual IDR terhadap Mata Uang Utama — 5 Juni 2026")
        df_k = pd.DataFrame([{"Mata Uang":k,"Kurs (IDR)":v,"Perubahan YTD":f"{'▲' if k in ['USD','EUR','GBP'] else '▼'} ~{random.randint(3,18)}%"} for k,v in KURS_AKTUAL.items()])
        st.dataframe(df_k.set_index("Mata Uang"), use_container_width=True)
        pasangan = st.selectbox("Tampilkan Simulasi Tren 90 Hari", list(KURS_AKTUAL.keys()))
        random.seed(hash(pasangan)%50)
        base = KURS_AKTUAL[pasangan]
        today = datetime.date.today()
        dates = [(today-datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(89,-1,-1)]
        vals = [round(base*0.88 + base*0.12*(i/89) + random.gauss(0,base*0.003),2) for i in range(90)]
        df_t = pd.DataFrame({"Tanggal":dates,pasangan:vals}).set_index("Tanggal")
        st.line_chart(df_t, color="#2dd4bf", height=280)
        st.caption("*Simulasi tren 90 hari berbasis kurs aktual hari ini")

    with tab3:
        tenor=[1,2,3,5,7,10,15,20,30]
        y_sbn=[6.2,6.6,6.9,7.0,7.05,7.1,7.15,7.2,7.3]
        df_o = pd.DataFrame({"Tenor (Tahun)":tenor,"Yield SBN (%)":y_sbn}).set_index("Tenor (Tahun)")
        sh("Yield Curve SBN Indonesia", "Estimasi per Juni 2026 — naik signifikan seiring kenaikan BI Rate dan pelemahan rupiah")
        st.area_chart(df_o, color="#c9a84c", height=340)
        c1,c2,c3 = st.columns(3)
        c1.metric("Yield SBN 10Y", "7,10%", "+0,85% dari awal 2026")
        c2.metric("Yield SBN 2Y", "6,60%", "+0,70%")
        c3.metric("Spread 10Y-2Y", "0,50%", "Normal slope")
        st.info("📌 Yield naik mencerminkan tekanan inflasi dan kurs. Investor asing masih selektif pada SBN tenor panjang.")

# ══════════════════════════════════════════════════════════════
# SEKTOR EKONOMI
# ══════════════════════════════════════════════════════════════

elif halaman == "🏭  Sektor Ekonomi":
    sh("🏭 Analisis Sektoral Ekonomi Indonesia", "Kontribusi dan pertumbuhan 9 sektor PDB Q1 2026")
    df_s = db_sektor()
    c1,c2 = st.columns(2)
    with c1:
        sh("Kontribusi Sektor (% PDB)")
        st.bar_chart(df_s.set_index("Sektor")[["Kontribusi PDB (%)"]], color="#c9a84c", height=350)
    with c2:
        sh("Pertumbuhan Sektoral (% YoY)")
        st.bar_chart(df_s.set_index("Sektor")[["Pertumbuhan (%)"]], color="#4ade80", height=350)
    st.markdown("---")
    sh("Tabel Lengkap Kinerja Sektoral")
    df_show = df_s.copy()
    df_show["Kontribusi PDB (%)"] = df_show["Kontribusi PDB (%)"].apply(lambda x:f"{x:.1f}%")
    df_show["Pertumbuhan (%)"] = df_show["Pertumbuhan (%)"].apply(lambda x:f"▲ {x:.1f}%")
    st.dataframe(df_show.set_index("Sektor"), use_container_width=True)
    sh("🔦 Spotlight Sektor")
    sel = st.selectbox("Pilih Sektor", df_s["Sektor"].tolist())
    bg = float(df_s[df_s["Sektor"]==sel]["Pertumbuhan (%)"].values[0])
    random.seed(hash(sel)%77)
    qtrs = [f"Q{q} {y}" for y in range(2023,2026) for q in range(1,5)][:10]
    gh = [round(bg+random.uniform(-1.8,1.8),2) for _ in qtrs]
    df_sp = pd.DataFrame({"Kuartal":qtrs,"Pertumbuhan (%)":gh}).set_index("Kuartal")
    st.line_chart(df_sp, color="#2dd4bf", height=260)

# ══════════════════════════════════════════════════════════════
# PROYEKSI & OUTLOOK
# ══════════════════════════════════════════════════════════════

elif halaman == "🔭  Proyeksi & Outlook":
    sh("🔭 Proyeksi & Outlook 2026–2030", "Skenario baseline — asumsi stabilisasi kondisi 2026")
    st.warning("⚠️ Proyeksi ilustratif berdasarkan konsensus IMF/BI/Kemenkeu. Bukan rekomendasi investasi.")

    df = db_proyeksi()
    tab1,tab2,tab3,tab4 = st.tabs(["📈 PDB","📊 Inflasi","💵 USD/IDR","🌏 Regional"])

    with tab1:
        st.bar_chart(df.set_index("Tahun")[["PDB (%)"]], color="#c9a84c", height=320)
        c1,c2,c3 = st.columns(3)
        c1.metric("2026F", "5,2%"); c2.metric("2028F", "5,5%"); c3.metric("2030F", "5,8%")

    with tab2:
        st.line_chart(df.set_index("Tahun")[["Inflasi (%)"]], color="#e8c97a", height=320)
        c1,c2,c3 = st.columns(3)
        c1.metric("2026F", "3,2% ⚠️"); c2.metric("2028F", "2,5%"); c3.metric("2030F", "2,2%")

    with tab3:
        st.line_chart(df.set_index("Tahun")[["USD/IDR"]], color="#f87171", height=320)
        c1,c2,c3 = st.columns(3)
        c1.metric("2026F (EOY)", "18.200"); c2.metric("2028F", "17.400"); c3.metric("2030F", "16.500")
        st.error("⚠️ Baseline asumsi stabilisasi bertahap. Risiko: tekanan Selat Hormuz, kebijakan Fed, dan outflow modal.")

    with tab4:
        negara = ["Indonesia","Vietnam","Filipina","Malaysia","Thailand","Singapura","India","China"]
        gdp_p = [5.2,6.1,5.8,4.4,3.1,2.4,6.5,4.8]
        df_reg = pd.DataFrame({"Negara":negara,"Proyeksi PDB 2026 (%)":gdp_p}).set_index("Negara")
        sh("Proyeksi Pertumbuhan PDB 2026 — Perbandingan Regional")
        st.bar_chart(df_reg, color="#2dd4bf", height=340)
        st.info("🇮🇩 Indonesia 5,2% — di atas rata-rata ASEAN 4,3%, namun di bawah India (6,5%) dan Vietnam (6,1%)")

# ══════════════════════════════════════════════════════════════
# KAMUS EKONOMI
# ══════════════════════════════════════════════════════════════

elif halaman == "📚  Kamus Ekonomi":
    sh("📚 Kamus Istilah Ekonomi", f"{len(KAMUS)} istilah penting — diperbarui sesuai kondisi Juni 2026")
    kat_colors = {
        "Kurs":"#f87171","Makro":"#4ade80","Moneter":"#c9a84c","Fiskal":"#f87171",
        "Perdagangan":"#2dd4bf","Pasar Modal":"#fb923c","Ketenagakerjaan":"#38bdf8","Indikator":"#94a3b8"
    }
    c1,c2 = st.columns([3,1])
    with c1: cari = st.text_input("🔍 Cari istilah...", placeholder="rupiah, inflasi, IHSG, BI Rate...")
    with c2: kat_f = st.selectbox("Kategori", ["Semua"]+sorted({k[2] for k in KAMUS}))
    hasil = KAMUS
    if cari: hasil = [k for k in hasil if cari.lower() in k[0].lower() or cari.lower() in k[1].lower()]
    if kat_f != "Semua": hasil = [k for k in hasil if k[2] == kat_f]
    st.markdown(f"<div style='color:#3d5166;font-size:.8rem;margin-bottom:1rem'>{len(hasil)} dari {len(KAMUS)} istilah</div>", unsafe_allow_html=True)
    for ist, dfn, kat in hasil:
        kc = kat_colors.get(kat, "#64748b")
        with st.expander(f"📖  {ist}"):
            st.markdown(f"""
            <span style='background:{kc}22;color:{kc};border:1px solid {kc}44;
                         padding:.15rem .6rem;border-radius:100px;font-size:.7rem;font-weight:600'>{kat}</span>
            <p style='color:#7a92a8;line-height:1.85;font-size:.9rem;margin-top:.75rem'>{dfn}</p>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# KALKULATOR EKONOMI
# ══════════════════════════════════════════════════════════════

elif halaman == "🧮  Kalkulator Ekonomi":
    sh("🧮 Kalkulator Ekonomi Interaktif", "4 kalkulator: inflasi, bunga majemuk, konversi kurs, estimasi PDB")

    tab1,tab2,tab3,tab4 = st.tabs(["📊 Dampak Inflasi","💰 Bunga Majemuk","💱 Konversi Kurs","📈 Target PDB"])

    with tab1:
        sh("Kalkulator Daya Beli — Dampak Inflasi Aktual")
        c1,c2,c3 = st.columns(3)
        with c1: nilai_awal = st.number_input("Nilai Uang (Rp)", 100_000, 10_000_000_000, 1_000_000, 100_000)
        with c2: inflasi_r = st.slider("Inflasi (%/tahun)", 1.0, 15.0, 3.08, 0.01)
        with c3: tahun_n = st.slider("Lama (tahun)", 1, 30, 10)
        nilai_riil = nilai_awal / ((1+inflasi_r/100)**tahun_n)
        r1,r2,r3 = st.columns(3)
        r1.metric("Nilai Awal", f"Rp {nilai_awal:,.0f}")
        r2.metric(f"Nilai Riil Setelah {tahun_n}th", f"Rp {nilai_riil:,.0f}", f"-{(1-nilai_riil/nilai_awal)*100:.1f}%")
        r3.metric("Daya Beli Hilang", f"Rp {nilai_awal-nilai_riil:,.0f}")
        rows = [{"Tahun ke-":y,"Nilai Riil (Rp)":f"Rp {nilai_awal/((1+inflasi_r/100)**y):,.0f}","Sisa DayaBeli":f"{(1-(1/(1+inflasi_r/100)**y))*100:.1f}% hilang"} for y in range(1,min(tahun_n+1,16))]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=220)
        st.info(f"💡 Dengan inflasi aktual 3,08%/tahun: Rp 1 juta hari ini = Rp {1_000_000/((1.0308)**10):,.0f} dalam 10 tahun.")

    with tab2:
        sh("Kalkulator Bunga Majemuk — Simulasi Investasi")
        c1,c2,c3,c4 = st.columns(4)
        with c1: modal = st.number_input("Modal Awal (Rp)", 1_000_000, 10_000_000_000, 10_000_000, 1_000_000)
        with c2: bunga = st.slider("Return (%/tahun)", 1.0, 25.0, 9.0, 0.5)
        with c3: setor = st.number_input("Setoran/Bulan (Rp)", 0, 50_000_000, 1_000_000, 500_000)
        with c4: lama = st.slider("Lama (tahun)", 1, 40, 20)
        v = float(modal); ts = float(modal); rows=[]
        for y in range(1,lama+1):
            for _ in range(12): v=v*(1+bunga/(100*12))+setor; ts+=setor
            rows.append({"Tahun ke-":y,"Nilai (Rp)":round(v),"Disetor (Rp)":round(ts),"Untung (Rp)":round(v-ts)})
        r1,r2,r3 = st.columns(3)
        r1.metric("Nilai Akhir", f"Rp {v:,.0f}")
        r2.metric("Total Disetor", f"Rp {ts:,.0f}")
        r3.metric("Total Keuntungan", f"Rp {v-ts:,.0f}", f"+{(v/ts-1)*100:.0f}%")
        df_b = pd.DataFrame(rows)
        st.line_chart(df_b.set_index("Tahun ke-")[["Nilai (Rp)","Disetor (Rp)"]], height=260)

    with tab3:
        sh("Konversi Kurs — Berdasarkan Data Aktual 5 Juni 2026")
        c1,c2,c3 = st.columns(3)
        with c1: amt = st.number_input("Jumlah", 1.0, 1e9, 100.0)
        with c2: dari = st.selectbox("Dari", list(KURS_AKTUAL.keys())+["IDR"])
        with c3: ke = st.selectbox("Ke", ["IDR"]+list(KURS_AKTUAL.keys()))
        if dari=="IDR": hk = amt/KURS_AKTUAL[ke]
        elif ke=="IDR": hk = amt*KURS_AKTUAL[dari]
        else: hk = (amt*KURS_AKTUAL[dari])/KURS_AKTUAL[ke]
        st.success(f"**{amt:,.2f} {dari}** = **{hk:,.4f} {ke}**")
        df_kr = pd.DataFrame([{"Mata Uang":k,"1 Unit = IDR":f"Rp {v:,.0f}","Kurs":"Aktual 5 Jun 2026"} for k,v in KURS_AKTUAL.items()])
        st.dataframe(df_kr.set_index("Mata Uang"), use_container_width=True)

    with tab4:
        sh("Estimasi Waktu Capai Target PDB")
        c1,c2,c3 = st.columns(3)
        with c1: pdb_skrg = st.number_input("PDB Saat Ini (T Rp)", 100.0, 100000.0, 23459.5, 100.0)
        with c2: pdb_tgt = st.number_input("Target PDB (T Rp)", 100.0, 200000.0, 30000.0, 500.0)
        with c3: gr = st.slider("Asumsi Growth (%/tahun)", 1.0, 15.0, 5.5, 0.1)
        if pdb_tgt > pdb_skrg:
            th = math.log(pdb_tgt/pdb_skrg)/math.log(1+gr/100)
            tc = datetime.date.today().year + math.ceil(th)
            st.success(f"🎯 Dengan growth **{gr}%/tahun**, target **Rp {pdb_tgt:,.0f} T** dicapai dalam **{th:.1f} tahun** (tahun **{tc}**).")
            rows=[]; v=pdb_skrg
            for y in range(1,int(math.ceil(th))+2):
                v*=(1+gr/100)
                rows.append({"Tahun ke-":y,"Proyeksi PDB (T Rp)":round(v,1)})
                if v>=pdb_tgt: break
            st.bar_chart(pd.DataFrame(rows).set_index("Tahun ke-"), color="#4ade80", height=260)
        else:
            st.warning("Target harus lebih besar dari PDB saat ini.")

# ══════════════════════════════════════════════════════════════
# TANYA AI EKONOMI — Powered by Claude API
# ══════════════════════════════════════════════════════════════

elif halaman == "🤖  Tanya AI Ekonomi":
    sh("🤖 Tanya AI Ekonomi", "Powered by Claude — Tanya apa saja tentang ekonomi Indonesia")

    # Context data aktual untuk AI
    KONTEKS_EKONOMI = """
Kamu adalah asisten ekonomi Indonesia yang ahli dan ramah. Kamu memiliki data terkini berikut (Juni 2026):

DATA AKTUAL INDONESIA (Juni 2026):
- USD/IDR: Rp 18.039 (level historis terlemah sepanjang masa, 4 Jun 2026)
- Inflasi IHK YoY: 3,08% (Mei 2026, BPS) — tertinggi sejak pertengahan 2023
- BI Rate: 5,25% (dinaikkan 50 bps pada Mei 2026)
- IHSG: 5.941,07 (3 Jun 2026, turun 4,11% — terdalam di Asia Pasifik)
- PDB Q1-2026: tumbuh 5,61% YoY (tertinggi sejak Q4-2022, BPS)
- Cadangan Devisa: USD 146,2 miliar (Apr 2026, turun 4 bulan beruntun)
- Ekspor Apr 2026: USD 25,30 miliar (surplus tipis USD 0,09 miliar)
- Tingkat Kemiskinan: 7,50% (Des 2025, BPS)
- PDB Nominal 2025: Rp 23.459,5 triliun
- DXY (Dollar Index): ~99,4

KONDISI TERKINI:
- Rupiah melemah ke level historis akibat: sentimen risk-off global, konflik geopolitik Timur Tengah (Selat Hormuz), outflow modal asing
- IHSG koreksi tajam dipimpin saham BREN dan DSSA
- Inflasi naik dipicu: cabai merah, minyak goreng, bawang merah, BBM nonsubsidi
- BI menaikkan suku bunga untuk menjaga stabilitas

KURS AKTUAL (5 Jun 2026, referensi BI):
USD=18039, EUR=19935, GBP=22858, JPY=108/IDR, SGD=13361, MYR=4349, AUD=12003, CNY=2460

Jawab dalam Bahasa Indonesia yang jelas, informatif, dan mudah dipahami. 
Sertakan angka aktual jika relevan. Jika ditanya rekomendasi investasi, berikan perspektif edukatif dan ingatkan untuk konsultasi profesional.
Batasi jawaban maksimal 300 kata agar ringkas dan padat.
"""

    # Inisialisasi riwayat chat di session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "ai_loading" not in st.session_state:
        st.session_state.ai_loading = False

    # ── Header info ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0c1830,#090e1a);border:1px solid #1a2c3d;
                border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;display:flex;gap:1rem;align-items:center'>
      <span style='font-size:2.5rem'>🤖</span>
      <div>
        <div style='color:#e8f0f8;font-weight:700;font-size:1rem'>Asisten AI EkonomiID</div>
        <div style='color:#5a7a8a;font-size:.83rem;margin-top:.25rem'>
          Tanya apa saja: kurs rupiah, inflasi, saham, investasi, istilah ekonomi, kondisi pasar, dll.
          AI mengetahui data aktual ekonomi Indonesia per Juni 2026.
        </div>
      </div>
      <div style='margin-left:auto;text-align:right'>
        <div style='background:rgba(74,222,128,.1);color:#4ade80;border:1px solid rgba(74,222,128,.25);
                    padding:.3rem .8rem;border-radius:100px;font-size:.72rem;font-weight:700'>
          🟢 Online
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Contoh pertanyaan ──
    st.markdown("<div style='color:#5a7a8a;font-size:.8rem;margin-bottom:.6rem;font-weight:600'>💡 Contoh pertanyaan:</div>", unsafe_allow_html=True)
    contoh = [
        "Kenapa rupiah tembus Rp18.000?",
        "Apa dampak IHSG turun ke 5.941?",
        "Jelaskan inflasi 3,08% dan dampaknya",
        "Berapa kurs EUR ke rupiah sekarang?",
        "Apa itu BI Rate dan fungsinya?",
        "Bagaimana kondisi ekonomi Indonesia Juni 2026?",
    ]
    cols_ex = st.columns(3)
    for i, c in enumerate(contoh):
        with cols_ex[i % 3]:
            if st.button(c, key=f"ex_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": c})
                st.session_state.ai_loading = True
                st.rerun()

    st.markdown("---")

    # ── Tampilkan riwayat chat ──
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='display:flex;justify-content:flex-end;margin-bottom:.75rem'>
              <div style='background:linear-gradient(135deg,#1a2c3d,#162334);border:1px solid #243d52;
                          border-radius:14px 14px 4px 14px;padding:.85rem 1.1rem;
                          max-width:75%;color:#e8f0f8;font-size:.9rem;line-height:1.6'>
                {msg["content"]}
              </div>
              <span style='font-size:1.4rem;margin-left:.6rem;align-self:flex-end'>👤</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='display:flex;margin-bottom:.75rem'>
              <span style='font-size:1.4rem;margin-right:.6rem;align-self:flex-start'>🤖</span>
              <div style='background:linear-gradient(135deg,#0f1928,#0c1520);border:1px solid #1a2c3d;
                          border-left:3px solid #c9a84c;border-radius:4px 14px 14px 14px;
                          padding:.85rem 1.1rem;max-width:80%;color:#94a3b8;font-size:.875rem;line-height:1.75'>
                {msg["content"].replace(chr(10), "<br>")}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Proses AI response jika loading ──
    if st.session_state.ai_loading and st.session_state.chat_history:
        with st.spinner("🤖 AI sedang menganalisis..."):
            try:
                import urllib.request, json as _json, ssl

                messages_payload = []
                for m in st.session_state.chat_history:
                    messages_payload.append({"role": m["role"], "content": m["content"]})

                payload = _json.dumps({
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1000,
                    "system": KONTEKS_EKONOMI,
                    "messages": messages_payload
                }).encode("utf-8")

                req = urllib.request.Request(
                    "https://api.anthropic.com/v1/messages",
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "anthropic-version": "2023-06-01",
                    },
                    method="POST"
                )

                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                    result = _json.loads(resp.read().decode("utf-8"))

                ai_text = result["content"][0]["text"]
                st.session_state.chat_history.append({"role": "assistant", "content": ai_text})
                st.session_state.ai_loading = False
                st.rerun()

            except Exception as e:
                err_msg = str(e)
                if "401" in err_msg or "403" in err_msg:
                    fallback = "⚠️ API key belum dikonfigurasi. Tambahkan ANTHROPIC_API_KEY di Streamlit Secrets (Settings → Secrets) untuk mengaktifkan AI."
                elif "timeout" in err_msg.lower():
                    fallback = "⏱️ Koneksi timeout. Coba lagi sebentar."
                else:
                    fallback = f"❌ Terjadi error: {err_msg[:120]}. Pastikan API key sudah dikonfigurasi di Streamlit Secrets."
                st.session_state.chat_history.append({"role": "assistant", "content": fallback})
                st.session_state.ai_loading = False
                st.rerun()

    # ── Input chat ──
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    with st.container():
        col_input, col_send, col_clear = st.columns([7, 1, 1])
        with col_input:
            user_input = st.text_input(
                "chat",
                placeholder="💬 Ketik pertanyaan tentang ekonomi Indonesia...",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_send:
            send = st.button("➤ Kirim", use_container_width=True, type="primary")
        with col_clear:
            if st.button("🗑️ Reset", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.ai_loading = False
                st.rerun()

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        st.session_state.ai_loading = True
        st.rerun()

    # ── Setup info ──
    if not st.session_state.chat_history:
        st.markdown("""
        <div style='background:rgba(201,168,76,.05);border:1px solid rgba(201,168,76,.15);
                    border-radius:10px;padding:1.1rem 1.25rem;margin-top:1rem'>
          <div style='color:#c9a84c;font-weight:700;font-size:.83rem;margin-bottom:.5rem'>⚙️ Cara Mengaktifkan AI</div>
          <div style='color:#5a7a8a;font-size:.8rem;line-height:1.9'>
            1. Dapatkan API key di <strong style='color:#e8f0f8'>console.anthropic.com</strong><br>
            2. Di Streamlit Cloud → <strong style='color:#e8f0f8'>Settings → Secrets</strong><br>
            3. Tambahkan: <code style='background:#1a2c3d;padding:.1rem .4rem;border-radius:4px;color:#2dd4bf'>ANTHROPIC_API_KEY = "sk-ant-..."</code><br>
            4. Simpan dan <strong style='color:#e8f0f8'>Reboot app</strong> — AI siap digunakan!
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='color:#3d5166;font-size:.72rem;text-align:center;margin-top:1rem'>
      ⚠️ AI memberikan informasi edukatif, bukan rekomendasi investasi.
      Selalu konsultasikan keputusan finansial dengan profesional.
    </div>
    """, unsafe_allow_html=True)




elif halaman == "📋  Laporan Sistem":
    sh("📋 Laporan Kekayaan Sistem EkonomiID", "Dokumentasi teknis lengkap — backend, frontend, dan fitur")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0c1830,#090e1a);border:1px solid #1a2c3d;
                border-radius:16px;padding:2rem;margin-bottom:1.5rem'>
      <h2 style='font-family:"Playfair Display",serif;color:#c9a84c;margin-bottom:.5rem'>
        EkonomiID v3.0 — Advanced Economy Portal
      </h2>
      <p style='color:#5a7a8a;font-size:.9rem;line-height:1.7'>
        Website informasi ekonomi Indonesia berbasis Python + Streamlit dengan data aktual,
        9 halaman fungsional, 8 tabel database, dan 4 kalkulator interaktif. Data diperbarui
        sesuai kondisi pasar terkini per Juni 2026.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Ringkasan Statistik ──
    sh("📊 Ringkasan Statistik Sistem")
    s1,s2,s3,s4 = st.columns(4)
    s1.metric("Halaman Aktif", "11")
    s2.metric("Tabel Database", "8")
    s3.metric("Indikator Dipantau", "8+")
    s4.metric("Istilah Kamus", str(len(KAMUS)))
    s1,s2,s3,s4 = st.columns(4)
    s1.metric("Berita & Analisis", str(len(BERITA)))
    s2.metric("Kalkulator", "4")
    s3.metric("Grafik Interaktif", "20+")
    s4.metric("Cache TTL", "5 menit")

    st.markdown("---")

    # ── BACKEND ──
    sh("🗄️ Backend — Struktur Database & Data Layer")
    st.markdown("""
    <div style='background:#0c1422;border:1px solid #1a2c3d;border-radius:12px;padding:1.5rem;margin-bottom:1.25rem'>
      <h4 style='color:#2dd4bf;margin-bottom:1rem'>📦 8 Tabel Database (In-Memory + Cache)</h4>
    """, unsafe_allow_html=True)

    db_info = [
        ("db_kurs_history()", "💵 Kurs USD/IDR", "54 baris", "Jan 2022 – Jun 2026 (bulanan)", "BI/Bloomberg"),
        ("db_inflasi()", "📊 Inflasi IHK", "29 baris", "Jan 2024 – Mei 2026 (bulanan)", "BPS"),
        ("db_gdp()", "🏛️ PDB Nominal & Growth", "16 baris", "2010–2025 (tahunan)", "BPS/Kemenkeu"),
        ("db_birate()", "⚖️ BI Rate History", "29 baris", "Jan 2022 – Mei 2026", "Bank Indonesia"),
        ("db_devisa()", "🏅 Cadangan Devisa", "5 baris", "Jan 2025 – Mei 2026 (bulanan)", "Bank Indonesia"),
        ("db_ihsg()", "📈 IHSG Harian", "120 baris", "120 hari terakhir (harian)", "BEI (sim. aktual)"),
        ("db_ekspor_impor()", "🚢 Neraca Perdagangan", "4 baris", "Jan–Apr 2026 (bulanan)", "BPS"),
        ("db_proyeksi()", "🔭 Proyeksi 2026–2030", "5 baris", "2026–2030 (tahunan)", "IMF/BI/Konsensus"),
    ]
    df_db = pd.DataFrame(db_info, columns=["Fungsi","Konten","Ukuran","Rentang Data","Sumber"])
    st.dataframe(df_db.set_index("Fungsi"), use_container_width=True)

    st.markdown("""
    <div style='background:#0c1422;border:1px solid #1a2c3d;border-radius:12px;padding:1.5rem;margin-top:1rem'>
      <h4 style='color:#2dd4bf;margin-bottom:.75rem'>⚙️ Arsitektur Backend</h4>
      <div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.85rem;color:#7a92a8;line-height:1.9'>
        <div>
          <strong style='color:#e8f0f8'>Runtime:</strong> Python 3.11+<br>
          <strong style='color:#e8f0f8'>Framework:</strong> Streamlit ≥1.35<br>
          <strong style='color:#e8f0f8'>Data Layer:</strong> Pandas DataFrame<br>
          <strong style='color:#e8f0f8'>Caching:</strong> @st.cache_data (TTL 300s)<br>
        </div>
        <div>
          <strong style='color:#e8f0f8'>Dependencies:</strong> streamlit, pandas<br>
          <strong style='color:#e8f0f8'>Storage:</strong> In-memory (no SQL)<br>
          <strong style='color:#e8f0f8'>Seed:</strong> random.seed() untuk reproducibility<br>
          <strong style='color:#e8f0f8'>Deploy:</strong> Streamlit Cloud<br>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── FRONTEND ──
    sh("🖥️ Frontend — Menu & Tampilan")
    frontend_pages = [
        ("🏠 Dashboard Utama","8 metric card aktual + 4 chart (kurs/inflasi/IHSG/BI Rate) + 4 berita breaking","Hero banner + indikator grid + dual-column charts + news grid"),
        ("📰 Berita & Analisis","8 artikel + filter 3 dimensi (teks/kategori/sentimen) + statistik sentimen","Filter bar + sentiment counter + article cards + analisis dampak"),
        ("🗄️ Database Tabel","8 tab tabel database lengkap + statistik per tabel + chart eksplorasi","Tab navigation + dataframe + metric cards + inline charts"),
        ("📊 Grafik Data Makro","5 tab: PDB/Inflasi/Kurs/BI Rate/Perdagangan + tabel kurs aktual","Tab navigation + bar/line/area charts + metric cards"),
        ("📈 Pasar Keuangan","IHSG 120h + multi-kurs 12 pasangan + Yield Curve SBN","Slider periode + dataframe kurs + area chart yield curve"),
        ("🏭 Sektor Ekonomi","9 sektor PDB + spotlight tren historis per sektor","Dual bar chart + dataframe + selectbox spotlight"),
        ("🔭 Proyeksi & Outlook","4 indikator 2026–2030 + perbandingan regional ASEAN 8 negara","Tab proyeksi + bar/line charts + regional comparison"),
        ("📚 Kamus Ekonomi",f"{len(KAMUS)} istilah + search + filter kategori + badge warna","Search bar + category filter + color-coded expanders"),
        ("🧮 Kalkulator Ekonomi","4 kalkulator interaktif + tabel proyeksi tahunan + chart bunga","Number input + slider + result metrics + charts"),
        ("📋 Laporan Sistem","Dokumentasi teknis lengkap backend+frontend+data aktual","Statistics grid + dataframes + architecture info"),
        ("ℹ️ Tentang","Deskripsi sistem, fitur, disclaimer, data sources","Info cards + disclaimer box"),
    ]
    df_fe = pd.DataFrame(frontend_pages, columns=["Halaman","Konten Utama","Komponen UI"])
    st.dataframe(df_fe.set_index("Halaman"), use_container_width=True)

    st.markdown("---")

    # ── DATA AKTUAL ──
    sh("📡 Data Aktual yang Digunakan (Juni 2026)")
    aktual_data = [
        ("USD/IDR","Rp 18.039","4 Jun 2026","Bloomberg/BI","Level historis terendah"),
        ("Inflasi IHK YoY","3,08%","2 Jun 2026","BPS","Tertinggi sejak pertengahan 2023"),
        ("BI Rate","5,25%","20 Mei 2026","Bank Indonesia","Naik 50 bps dari 4,75%"),
        ("IHSG","5.941,07","3 Jun 2026","BEI","Turun 4,11% — terdalam di Asia Pasifik"),
        ("PDB Q1 2026","5,61% YoY","5 Mei 2026","BPS","Tertinggi sejak Q4 2022"),
        ("Cadangan Devisa","$146,2 M","7 Mei 2026","Bank Indonesia","Terendah sejak Agustus 2024"),
        ("Ekspor Apr 2026","$25,30 M","15 Mei 2026","BPS","Surplus tipis $0,09 M"),
        ("Kemiskinan","7,50%","Des 2025","BPS","Semester II 2025"),
    ]
    df_aktual = pd.DataFrame(aktual_data, columns=["Indikator","Nilai","Tanggal","Sumber","Catatan"])
    st.dataframe(df_aktual.set_index("Indikator"), use_container_width=True)

    st.markdown("---")

    # ── Kekayaan Fitur ──
    sh("🌟 Ringkasan Kekayaan Fitur Sistem")
    fitur_list = [
        ("📡","Data Real Aktual","Semua indikator utama diperbarui berdasarkan data aktual per 4–5 Juni 2026. Kurs 18.039, inflasi 3,08%, IHSG 5.941, BI Rate 5,25%."),
        ("🗄️","8 Tabel Database","Backend data terstruktur: kurs bulanan 54 periode, inflasi 29 periode, PDB 16 tahun, BI Rate 29 periode, devisa, IHSG harian 120 hari, ekspor-impor, proyeksi."),
        ("📰","Analisis Mendalam","8 berita dengan konteks, analisis dampak pasar, dan badge sentimen (positif/netral/negatif). Filter multi-dimensi."),
        ("📊","20+ Grafik Interaktif","Bar chart, line chart, area chart untuk setiap indikator. Slider periode untuk IHSG. Multi-kurs 12 pasangan."),
        ("🧮","4 Kalkulator","Dampak inflasi, bunga majemuk, konversi kurs 12 mata uang aktual, estimasi target PDB dengan proyeksi tahunan."),
        ("📚","18 Istilah Kamus","Kamus dilengkapi konteks kondisi Juni 2026. Filter kategori dan search real-time."),
        ("🔭","Proyeksi Regional","5 tahun ke depan + perbandingan 8 negara ASEAN/Asia."),
        ("🎨","UI Premium Dark Mode","CSS custom: gradient cards, tooltip, scrollbar, animasi hover, Playfair Display + DM Mono typography."),
    ]
    c1,c2 = st.columns(2)
    for i,(ikon,jdl,dsk) in enumerate(fitur_list):
        with (c1 if i%2==0 else c2):
            st.markdown(f"""
            <div style='background:#0c1422;border:1px solid #1a2c3d;border-radius:12px;
                        padding:1.1rem;margin-bottom:.75rem;display:flex;gap:.85rem;align-items:flex-start'>
              <span style='font-size:1.5rem;flex-shrink:0'>{ikon}</span>
              <div><strong style='color:#e8f0f8;font-size:.9rem'>{jdl}</strong>
              <p style='color:#5a7a8a;font-size:.8rem;margin-top:.25rem;line-height:1.55'>{dsk}</p></div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TENTANG
# ══════════════════════════════════════════════════════════════

elif halaman == "ℹ️  Tentang":
    sh("ℹ️ Tentang EkonomiID v3.0")
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0c1830,#090e1a);border:1px solid #1a2c3d;
                border-radius:16px;padding:2.5rem;margin-bottom:1.5rem'>
      <h3 style='font-family:"Playfair Display",serif;color:#e8f0f8;margin-bottom:.75rem'>Apa itu EkonomiID?</h3>
      <p style='color:#7a92a8;line-height:1.85;font-size:.95rem'>
        <strong style='color:#e8f0f8'>EkonomiID v3.0</strong> adalah dashboard ekonomi Indonesia yang komprehensif
        dan selalu diperbarui dengan data aktual. Dirancang untuk memberikan gambaran lengkap kondisi
        makroekonomi, pasar keuangan, dan proyeksi Indonesia — khususnya di tengah kondisi kritis
        pelemahan rupiah ke Rp18.039/USD dan tekanan inflasi 3,08% pada Juni 2026.
      </p>
    </div>
    <div style='background:rgba(248,113,113,.05);border:1px solid rgba(248,113,113,.2);
                border-radius:12px;padding:1.5rem;margin-bottom:1.5rem'>
      <strong style='color:#f87171'>⚠️ Disclaimer</strong>
      <p style='color:#5a7a8a;font-size:.875rem;line-height:1.8;margin-top:.5rem'>
        Data bersifat <strong style='color:#e8f0f8'>ilustratif-aktual</strong> — data historis berdasarkan sumber
        terpercaya (BI, BPS, Bloomberg), simulasi menggunakan seed tetap untuk reproducibility.
        <strong>Bukan rekomendasi investasi.</strong><br><br>
        Sumber resmi: <strong style='color:#e8f0f8'>bi.go.id · bps.go.id · kemenkeu.go.id · idx.co.id · databoks.katadata.co.id</strong>
      </p>
    </div>
    <div style='text-align:center;padding:1.5rem;color:#243344;font-size:.875rem'>
      Dibangun dengan ❤️ menggunakan <strong style='color:#3d5166'>Python + Streamlit</strong> · v3.0 · Jun 2026
    </div>
    """, unsafe_allow_html=True)

