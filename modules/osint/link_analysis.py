from pyrogram import Client, filters
from pyrogram.types import Message
from core.config import Config
from utils.validators import is_valid_url
import requests
import logging
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

@Client.on_message(filters.regex(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+") & filters.private)
async def link_analyzer(client: Client, message: Message):
    urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", message.text)
    if not urls:
        return

    url = urls[0] # Ambil URL pertama yang ditemukan
    if not is_valid_url(url):
        return # Abaikan jika bukan URL valid

    await message.reply_text(f"Menganalisis tautan: `{url}`...", quote=True)

    analysis_results = []

    # 1. Pratinjau Tautan (Link Preview)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml') # Menggunakan lxml untuk parsing cepat

        title = soup.find('meta', property='og:title') or soup.find('title')
        description = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'description'})
        image = soup.find('meta', property='og:image')

        preview_text = "**Pratinjau Tautan:**\n"
        preview_text += f"Judul: {title.get('content') if title and title.get('content') else title.text if title else 'Tidak ada'}\n"
        preview_text += f"Deskripsi: {description.get('content') if description and description.get('content') else 'Tidak ada'}\n"
        preview_text += f"URL Gambar: {image.get('content') if image and image.get('content') else 'Tidak ada'}\n"
        analysis_results.append(preview_text)

    except requests.exceptions.RequestException as e:
        log.warning(f"Failed to get link preview for {url}: {e}")
        analysis_results.append(f"Gagal mendapatkan pratinjau tautan: {e}")
    except Exception as e:
        log.warning(f"Error parsing link preview for {url}: {e}")
        analysis_results.append(f"Kesalahan saat memparsing pratinjau tautan: {e}")

    # 2. VirusTotal API Check
    if Config.VIRUSTOTAL_API_KEY:
        try:
            vt_url = "https://www.virustotal.com/api/v3/urls"
            headers = {"x-apikey": Config.VIRUSTOTAL_API_KEY}
            data = {"url": url}
            
            # Submit URL for analysis
            submit_response = requests.post(vt_url, headers=headers, data=data)
            submit_response.raise_for_status()
            analysis_id = submit_response.json()['data']['id']

            # Get analysis report (might need to poll in real app)
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            report_response = requests.get(report_url, headers=headers, timeout=15)
            report_response.raise_for_status()
            report_data = report_response.json()

            stats = report_data['data']['attributes']['stats']
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)
            undetected = stats.get('undetected', 0)

            vt_report_text = (
                f"**Analisis VirusTotal:**\n"
                f"Malicious: {malicious}\n"
                f"Suspicious: {suspicious}\n"
                f"Undetected: {undetected}\n"
                f"Lihat Laporan Lengkap: https://www.virustotal.com/gui/url/{analysis_id.split('-')[1]}/detection\n"
            )
            analysis_results.append(vt_report_text)

        except requests.exceptions.RequestException as e:
            log.error(f"VirusTotal API error for {url}: {e}")
            analysis_results.append(f"Gagal terhubung ke VirusTotal: {e}")
        except Exception as e:
            log.error(f"Error during VirusTotal analysis for {url}: {e}")
            analysis_results.append(f"Terjadi kesalahan saat menganalisis dengan VirusTotal: {e}")
    else:
        analysis_results.append("Kunci API VirusTotal tidak dikonfigurasi.")

    await message.reply_text("\n\n".join(analysis_results))