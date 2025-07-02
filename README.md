<p align="center">
  <img src="https://github.com/images/mona-whisper.gif" alt="Aetherbot Logo" width="150"/>
</p>

<h1 align="center"><b>Aetherbot - OSINT & Investigation Bot</b></h1>

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

---

## 🧠 Overview

**Aetherbot** adalah bot Telegram modular berbasis **Pyrogram** untuk tugas Open-Source Intelligence (OSINT) dan investigasi. Dengan arsitektur fleksibel, Aetherbot mampu mengumpulkan, menganalisis, dan melaporkan data dari Telegram maupun layanan eksternal.

---

## 🚀 Features

### 1. OSINT Capabilities

* `/userinfo <username/id>` — Info publik pengguna Telegram.
* `/channelinfo <username/id>` — Info publik grup atau channel.
* `/analyze_link <url>` — Analisis tautan (VirusTotal, pratinjau).
* `/reverse_image` *(reply photo)* — Pencarian gambar terbalik.
* `/hunterio <domain/email>` — Pencarian & validasi email (Hunter.io).
* `/hibp <email>` — Cek kebocoran data (HaveIBeenPwned).
* `/shodan <query/ip>` — Info perangkat (Shodan).

### 2. Investigation & Reporting

* `/newcase <judul>` — Buat kasus investigasi baru.
* `/add_evidence <case_id>` *(reply message)* — Tambah bukti.
* `/listcases` — Lihat semua kasus.
* `/viewcase <case_id>` — Lihat detail kasus.
* `/report <case_id>` — Hasilkan laporan PDF.

### 3. Admin & UX

* `/setadmin <user_id>` — Jadikan user sebagai admin.
* `/removeadmin <user_id>` — Hapus admin.
* `/listadmins` — Lihat daftar admin.
* `/monitor_keyword <chat_id> <keyword>` — Pantau kata kunci.
* `/stop_monitor <chat_id> <keyword>` — Hentikan pemantauan.
* `/help` — Bantuan umum.
* `/help osint`, `/help investigation`, `/help admin` — Bantuan spesifik.

---

## ⚙️ Setup

### 1. Clone Repository

```bash
git clone https://github.com/aes-co/aetherbot.git
cd aetherbot
```

Atau jika sudah ada folder proyek, gunakan struktur otomatis:

```bash
# contoh (buat folder manual)
mkdir core
mkdir -p modules/osint modules/investigation modules/admin modules/general
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Buat file `.env` di root proyek:

```ini
API_ID=YOUR_TELEGRAM_API_ID
API_HASH=YOUR_TELEGRAM_API_HASH
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
MONGO_URI=mongodb://localhost:27017/
LOG_CHANNEL_ID=-1001234567890
ADMIN_IDS=12345678,98765432

# Optional
VIRUSTOTAL_API_KEY=...
HUNTER_IO_API_KEY=...
SHODAN_API_KEY=...
HAVEIBEENPWNED_API_KEY=...
```

### 4. Run Bot

Pastikan MongoDB aktif lalu jalankan:

```bash
python main.py
```

---

## 📂 Project Structure

```
aetherbot/
├── core/             # Konfigurasi inti, DB, Pyrogram
├── modules/
│   ├── admin/        # Fitur admin
│   ├── general/      # Perintah umum
│   ├── investigation/# Manajemen kasus & bukti
│   └── osint/        # OSINT tools
├── utils/            # Fungsi bantu
├── models/           # Skema MongoDB
├── handlers/         # Handler Pyrogram
├── main.py           # Entry point
├── requirements.txt  # Dependencies
├── .env.example      # Contoh .env
├── Dockerfile        # Docker config
└── README.md         # Dokumentasi ini
```

---

## 🤝 Credits

* **[Pyrogram](https://github.com/pyrogram/pyrogram)** — Telegram API framework.
* **Kontributor Aetherbot** — Terima kasih untuk kontribusi kalian 💜

---

## 📄 License

This project is licensed under the **AGPL-3.0 License**.

---

## 📊 Want to Contribute?

Kami sangat terbuka untuk kontribusi! 💫

* Ketemu bug? **Buka issue**
* Punya fitur baru? **Buat diskusi**
* Mau kontribusi langsung? **Fork → commit → Pull Request**

Lihat label `good first issue` untuk pemula!

Berpartisipasi di Hacktoberfest? PR kamu dihitung juga!

---

<p align="center">
  <i>Made with ❤️ by <a href="https://github.com/aes-co">aes-co</a></i>
</p>
