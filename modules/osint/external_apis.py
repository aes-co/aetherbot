from pyrogram import Client, filters
from pyrogram.types import Message
from core.config import Config
from utils.validators import is_valid_url, is_valid_telegram_username, is_valid_telegram_id
import requests
import logging
import json
import re
import os
from modules.osint.reverse_image_scraper import search_image_on_google # Import fungsi baru

log = logging.getLogger(__name__)

# --- Hunter.io Integration ---
@Client.on_message(filters.command("hunterio") & filters.private)
async def hunter_io_check(client: Client, message: Message):
    """
    Performs email search or domain/email verification using Hunter.io.
    Usage: /hunterio <domain_or_email>
    """
    args = message.command
    if len(args) < 2:
        await message.reply_text("Usage: `/hunterio <domain_or_email>`")
        return

    target = args[1]
    if not Config.HUNTER_IO_API_KEY:
        await message.reply_text("Hunter.io API key is not configured.")
        return

    await message.reply_text(f"Searching Hunter.io for `{target}`...", quote=True)

    try:
        if "@" in target:
            api_url = f"https://api.hunter.io/v2/email-verifier?email={target}&api_key={Config.HUNTER_IO_API_KEY}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = data.get('data', {})
            status = result.get('status', 'N/A')
            score = result.get('score', 'N/A')
            disposable = result.get('disposable', 'N/A')
            mx_records = result.get('mx_records', 'N/A')

            await message.reply_text(
                f"**Hunter.io Email Verifier:**\n"
                f"Email: `{target}`\n"
                f"Status: {status}\n"
                f"Score: {score}\n"
                f"Disposable: {disposable}\n"
                f"MX Records: {mx_records}"
            )
        else:
            api_url = f"https://api.hunter.io/v2/domain-search?domain={target}&api_key={Config.HUNTER_IO_API_KEY}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            organization = data.get('data', {}).get('organization', 'N/A')
            emails = data.get('data', {}).get('emails', [])
            
            email_info = ""
            if emails:
                email_info = "\n".join([f"- {e['value']} ({e['type']})" for e in emails[:5]])
            else:
                email_info = "No public emails found."

            await message.reply_text(
                f"**Hunter.io Domain Search:**\n"
                f"Domain: `{target}`\n"
                f"Organization: {organization}\n\n"
                f"Emails Found:\n{email_info}"
            )

    except requests.exceptions.RequestException as e:
        log.error(f"Hunter.io API error for {target}: {e}")
        await message.reply_text(f"Failed to connect to Hunter.io: {e}")
    except Exception as e:
        log.error(f"Error during Hunter.io check for {target}: {e}")
        await message.reply_text(f"An error occurred while searching Hunter.io: {e}")

# --- HaveIBeenPwned (HIBP) Integration ---
@Client.on_message(filters.command("hibp") & filters.private)
async def have_i_been_pwned_check(client: Client, message: Message):
    """
    Searches for data breaches for an email using HaveIBeenPwned.
    Usage: /hibp <email>
    """
    args = message.command
    if len(args) < 2:
        await message.reply_text("Usage: `/hibp <email>`")
        return

    email = args[1]
    if not Config.HAVEIBEENPWNED_API_KEY:
        await message.reply_text("HaveIBeenPwned API key is not configured.")
        return

    await message.reply_text(f"Searching for data breaches for `{email}` on HaveIBeenPwned...", quote=True)

    try:
        headers = {"User-Agent": "Aetherbot", "hibp-api-key": Config.HAVEIBEENPWNED_API_KEY}
        api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        response = requests.get(api_url, headers=headers, timeout=10)

        if response.status_code == 404:
            await message.reply_text(f"Email `{email}` not found in any known data breaches.")
        elif response.status_code == 200:
            breaches = response.json()
            if breaches:
                breach_names = [b['Name'] for b in breaches]
                await message.reply_text(
                    f"Email `{email}` found in the following data breaches:\n" + 
                    "\n".join(breach_names)
                )
            else:
                await message.reply_text(f"Email `{email}` not found in any known data breaches.")
        else:
            await message.reply_text(f"An error occurred while checking HIBP: Status {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        log.error(f"HIBP API error for {email}: {e}")
        await message.reply_text(f"Failed to connect to HaveIBeenPwned: {e}")
    except Exception as e:
        log.error(f"Error during HIBP check for {email}: {e}")
        await message.reply_text(f"An error occurred while checking HIBP: {e}")

# --- Shodan Integration ---
@Client.on_message(filters.command("shodan") & filters.private)
async def shodan_search_command(client: Client, message: Message):
    """
    Performs a Shodan search for a specific IP or query.
    Usage: /shodan <query_or_ip>
    """
    args = message.command
    if len(args) < 2:
        await message.reply_text("Usage: `/shodan <query_or_ip>`")
        return

    query = " ".join(args[1:])
    if not Config.SHODAN_API_KEY:
        await message.reply_text("Shodan API key is not configured.")
        return

    await message.reply_text(f"Searching Shodan for `{query}`...", quote=True)

    try:
        api_url = f"https://api.shodan.io/shodan/host/search?key={Config.SHODAN_API_KEY}&query={query}"
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", query):
            api_url = f"https://api.shodan.io/shodan/host/{query}?key={Config.SHODAN_API_KEY}"
        
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", query):
            if data:
                ports = ", ".join(map(str, data.get('ports', [])))
                org = data.get('org', 'N/A')
                country = data.get('country_name', 'N/A')
                await message.reply_text(
                    f"**Shodan Host Info for {query}:**\n"
                    f"Organization: {org}\n"
                    f"Country: {country}\n"
                    f"Open Ports: {ports}\n"
                    f"Shodan Link: https://www.shodan.io/host/{query}"
                )
            else:
                await message.reply_text(f"No information found on Shodan for IP `{query}`.")
        else:
            matches = data.get('matches', [])
            if matches:
                result_text = f"**Shodan Search Results for `{query}`:**\n"
                for i, host in enumerate(matches[:5]):
                    ip_str = host.get('ip_str', 'N/A')
                    org = host.get('org', 'N/A')
                    port_count = len(host.get('ports', []))
                    result_text += (
                        f"\n`{i+1}.` IP: `{ip_str}`\n"
                        f"   Organization: {org}\n"
                        f"   Open Ports: {port_count}\n"
                        f"   Link: https://www.shodan.io/host/{ip_str}"
                    )
                await message.reply_text(result_text)
            else:
                await message.reply_text(f"No results found on Shodan for query `{query}`.")

    except requests.exceptions.RequestException as e:
        log.error(f"Shodan API error for {query}: {e}")
        await message.reply_text(f"Failed to connect to Shodan: {e}")
    except Exception as e:
        log.error(f"Error during Shodan search for {query}: {e}")
        await message.reply_text(f"An error occurred while searching Shodan: {e}")

# --- Reverse Image Search ---
@Client.on_message(filters.command("reverse_image") & filters.private & filters.reply)
async def reverse_image_search_command(client: Client, message: Message):
    """
    Performs a reverse image search using web scraping. Requires replying to a message containing a photo.
    Usage: /reverse_image (reply to a photo)
    """
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Please reply to a message containing a photo to perform a reverse image search.")
        return

    photo = message.reply_to_message.photo
    await message.reply_text("Performing reverse image search using web scraping...", quote=True)

    temp_photo_path = None
    try:
        temp_photo_path = await client.download_media(photo)
        
        # Panggil fungsi scraping dari file terpisah
        results = await search_image_on_google(temp_photo_path)

        if results:
            response_text = "**Reverse Image Search Results:**\n\n"
            for i, result in enumerate(results[:5]): # Batasi 5 hasil
                response_text += f"{i+1}. **{result['title']}**\n"
                response_text += f"   URL: {result['url']}\n"
                if result['snippet']:
                    response_text += f"   Snippet: {result['snippet']}\n"
                response_text += "\n"
            await message.reply_text(response_text, disable_web_page_preview=True)
        else:
            await message.reply_text("No results found for the image via reverse image search.")

    except Exception as e:
        log.error(f"Error during reverse image search: {e}")
        await message.reply_text(f"An error occurred while performing reverse image search: {e}")
    finally:
        if temp_photo_path and os.path.exists(temp_photo_path):
            os.remove(temp_photo_path)
            log.info(f"Cleaned up temporary photo file: {temp_photo_path}")

