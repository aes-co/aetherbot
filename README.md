<p align="center">
<img src="https://placehold.co/150x150/ADD8E6/000000?text=Aetherbot+Logo" alt="Aetherbot Logo" width="150"/>
</p>

<h1 align="center">
<b>Aetherbot - OSINT & Investigation Bot</b>
</h1>

<p align="center">
A modular, fast, and powerful Telegram Bot built using Python and Pyrogram for OSINT and investigation tasks.
</p>

<p align="center">
<a href="https://github.com/aes-co/aetherbot"><img src="https://img.shields.io/github/stars/aes-co/aetherbot?style=flat-square&color=yellow" alt="Stars"/></a>
<a href="https://github.com/aes-co/aetherbot/fork"><img src="https://img.shields.io/github/forks/aes-co/aetherbot?style=flat-square&color=orange" alt="Forks"/></a>
<a href="https://github.com/aes-co/aetherbot"><img src="https://img.shields.io/github/repo-size/aes-co/aetherbot?style=flat-square&color=green" alt="Repo Size"/></a>
<img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square" alt="Python Version"/>
<img src="https://img.shields.io/badge/License-AGPL--3.0-lightgrey?style=flat-square" alt="License"/>
<img src="https://img.shields.io/badge/Maintained-Yes-brightgreen?style=flat-square" alt="Maintained"/>
<img src="https://img.shields.io/badge/good%20first%20issue-welcome-blueviolet?style=flat-square" alt="Good First Issue"/>
<img src="https://img.shields.io/badge/hacktoberfest-accepted-orange?style=flat-square" alt="Hacktoberfest"/>
</p>    
🧠 Overview

Aetherbot adalah bot Telegram modular yang dirancang untuk membantu dalam tugas-tugas Open-Source Intelligence (OSINT) dan investigasi. Dibangun menggunakan Pyrogram, Aetherbot menyediakan berbagai alat untuk mengumpulkan, menganalisis, dan melaporkan informasi dari sumber terbuka, terutama yang terkait dengan Telegram dan layanan eksternal lainnya.
🚀 Features

Berikut adalah perintah-perintah utama yang tersedia di Aetherbot:
1. Kapabilitas OSINT

    /userinfo <username_atau_id> — Dapatkan informasi publik pengguna Telegram.

    /channelinfo <username_atau_id> — Dapatkan informasi publik saluran atau grup Telegram.

    /analyze_link <url> — Pindai tautan untuk potensi ancaman (VirusTotal, pratinjau).

    /reverse_image (balas ke foto) — Lakukan pencarian gambar terbalik menggunakan web scraping.

    /hunterio <domain_atau_email> — Cari email terkait domain atau verifikasi alamat email via Hunter.io.

    /hibp <email> — Periksa kebocoran data untuk alamat email via HaveIBeenPwned.

    /shodan <query_atau_ip> — Cari perangkat yang terhubung ke internet via Shodan.

2. Fitur Investigasi & Pelaporan

    /newcase <judul_kasus> — Buat kasus investigasi baru.

    /add_evidence <case_id> (balas ke pesan) — Tambahkan pesan/media sebagai bukti ke kasus.

    /listcases — Lihat daftar kasus investigasi Anda.

    /viewcase <case_id> — Lihat detail dan bukti dalam kasus.

    /report <case_id> — Hasilkan laporan PDF komprehensif untuk kasus.

3. Peningkatan Pengalaman Pengguna & Administrasi

    /setadmin <user_id> — Atur pengguna sebagai admin.

    /removeadmin <user_id> — Hapus pengguna dari admin.

    /listadmins — Daftar semua admin yang terdaftar.

    /monitor_keyword <chat_id> <keyword> — Mulai memantau kata kunci di grup/saluran publik.

    /stop_monitor <chat_id> <keyword> — Hentikan pemantauan kata kunci tertentu.

    /help — Bantuan umum.

    /help osint — Bantuan khusus OSINT.

    /help investigation — Bantuan khusus investigasi.

    /help admin — Bantuan khusus admin.

⚙️ Setup
1. Klon Repositori (atau Buat Struktur Manual)

Jika Anda belum melakukannya, klon repositori Aetherbot atau buat struktur folder seperti yang telah kita diskusikan. Pastikan Anda berada di direktori tempat Anda ingin folder aetherbot dibuat, lalu jalankan script setup otomatis yang telah kita buat sebelumnya:

# Jika Anda ingin membuat folder aetherbot baru:
git clone https://github.com/aes-co/aetherbot.git
cd aetherbot

# Atau jika Anda sudah di dalam folder proyek yang ingin digunakan,
# jalankan script setup otomatis yang telah kita buat sebelumnya (dari percakapan ini).
# Contoh bagian awal script:
# #!/bin/bash
# mkdir core
# mkdir -p modules/osint modules/investigation modules/admin modules/general
# ... dst

2. Instal Dependensi Python

Pastikan Anda berada di direktori root proyek (aetherbot/).

pip install -r requirements.txt

3. Konfigurasi Variabel Lingkungan (.env)

Buat file bernama .env di direktori root proyek Anda (sejajar dengan main.py). Jangan pernah meng-commit file ini ke Git!

Isi file .env dengan kredensial Anda:

API_ID=YOUR_TELEGRAM_API_ID
API_HASH=YOUR_TELEGRAM_API_HASH
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
MONGO_URI=mongodb://localhost:27017/ # Ganti jika MongoDB Anda di cloud (misal: MongoDB Atlas URI)
LOG_CHANNEL_ID=-1001234567890 # ID saluran untuk log bot (dapatkan dari @JsonDumpBot)
ADMIN_IDS=12345678,98765432 # ID Telegram Anda dan admin lain, pisahkan koma

VIRUSTOTAL_API_KEY=YOUR_VIRUSTOTAL_API_KEY_HERE # Opsional
HUNTER_IO_API_KEY=YOUR_HUNTER_IO_API_KEY_HERE # Opsional
SHODAN_API_KEY=YOUR_SHODAN_API_KEY_HERE # Opsional
HAVEIBEENPWNED_API_KEY=YOUR_HAVEIBEENPWNED_API_KEY_HERE # Opsional

4. Jalankan Bot

Pastikan server MongoDB Anda sedang berjalan. Kemudian, dari direktori root proyek Anda, jalankan bot:

python main.py

Bot akan mulai berjalan dan Anda akan melihat log di terminal Anda.
📂 Struktur Proyek

Proyek Aetherbot diatur secara modular untuk kemudahan pengembangan dan pemeliharaan:

aetherbot/
├── core/                   # Konfigurasi inti, koneksi DB, klien Pyrogram, dekorator
├── modules/                # Modul fitur utama (OSINT, Investigasi, Admin, Umum)
│   ├── admin/              # Fitur admin (manajemen peran, monitoring)
│   ├── general/            # Perintah umum (help, start)
│   ├── investigation/      # Fitur manajemen kasus, bukti, dan laporan
│   └── osint/              # Fitur OSINT (info user/channel, analisis link, API eksternal)
├── utils/                  # Fungsi bantu, filter kustom, validator
├── models/                 # Definisi skema data untuk MongoDB (User, Case, Evidence)
├── handlers/               # Penanganan pesan dan perintah umum Pyrogram
├── main.py                 # Titik masuk utama aplikasi
├── requirements.txt        # Daftar dependensi Python
├── .env.example            # Contoh file variabel lingkungan
├── Dockerfile              # Konfigurasi Docker untuk deployment
└── README.md               # Dokumentasi proyek

🤝 Credits

    Pyrogram — Pustaka utama yang digunakan untuk berinteraksi dengan Telegram API.

    Kontributor Aetherbot — Terima kasih kepada semua yang berkontribusi pada proyek ini.

📄 License

Proyek ini dilisensikan di bawah AGPL-3.0 License.
📊 Want to Contribute?

Kami menyambut kontribusi dari komunitas! 🤩

    Menemukan bug? Buka issue.

    Punya ide fitur? Mulai diskusi.

    Ingin meningkatkan kode? Cukup fork repositori, push perubahan, dan buat Pull Request!

Kontribusi Anda sangat dihargai dan akan dikreditkan ✨

Mencari kontribusi pertama Anda? Lihat good first issues kami!

Berpartisipasi dalam Hacktoberfest? Pull Request Anda di sini dihitung!

<p align="center">Made with 💖 by aes-co</p>