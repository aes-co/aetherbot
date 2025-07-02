from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import logging
from core.decorators import registered_user, admin_only
from models.case import Case
from models.evidence import Evidence
from utils.helpers import format_timestamp

log = logging.getLogger(__name__)

@Client.on_callback_query(registered_user)
async def handle_callback_queries(client: Client, callback_query: CallbackQuery):
    """
    Menangani semua callback queries dari tombol inline keyboard.
    """
    data = callback_query.data
    user_id = callback_query.from_user.id
    message = callback_query.message
    chat_id = message.chat.id

    log.info(f"Received callback query from {user_id} in chat {chat_id}: {data}")

    try:
        # Contoh penanganan callback untuk manajemen kasus
        if data.startswith("view_case_"):
            case_id = data.split("_")[2]
            case = await Case.get_case(case_id)
            if not case or case.created_by != user_id:
                await callback_query.answer("Kasus tidak ditemukan atau Anda tidak memiliki akses.", show_alert=True)
                return

            evidence_list = await Evidence.get_evidence_by_case(case_id)

            case_detail_text = (
                f"**Detail Kasus: {case.title}**\n"
                f"ID Kasus: `{case.case_id}`\n"
                f"Status: {case.status.capitalize()}\n"
                f"Dibuat Oleh: `{case.created_by}`\n"
                f"Dibuat Pada: {format_timestamp(case.created_at)}\n"
                f"Deskripsi: {case.description if case.description else 'Tidak ada'}\n\n"
                f"**Daftar Bukti ({len(evidence_list)}):**\n"
            )

            if not evidence_list:
                case_detail_text += "Tidak ada bukti yang ditambahkan ke kasus ini."
            else:
                for i, evidence in enumerate(evidence_list):
                    case_detail_text += (
                        f"  `{i+1}.` Tipe: {evidence.type.capitalize()}\n"
                        f"     Konten: {evidence.content[:50]}...\n"
                        f"     Ditambahkan: {format_timestamp(evidence.added_at)}\n"
                    )
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Hasilkan Laporan", callback_data=f"generate_report_{case_id}")],
                [InlineKeyboardButton("Tutup Kasus", callback_data=f"close_case_{case_id}")]
            ])
            await message.edit_text(case_detail_text, reply_markup=keyboard)
            await callback_query.answer("Detail kasus dimuat.")

        elif data.startswith("generate_report_"):
            case_id = data.split("_")[2]
            # Panggil fungsi generate report dari modules/investigation/report_generation.py
            # Asumsi ada fungsi yang bisa dipanggil secara eksternal
            from modules.investigation.report_generation import generate_report_for_case
            await callback_query.answer("Memulai pembuatan laporan...", show_alert=True)
            await generate_report_for_case(client, chat_id, case_id)
            await message.edit_reply_markup(reply_markup=None) # Hapus tombol setelah aksi

        elif data.startswith("close_case_"):
            case_id = data.split("_")[2]
            case = await Case.get_case(case_id)
            if not case or case.created_by != user_id:
                await callback_query.answer("Kasus tidak ditemukan atau Anda tidak memiliki akses.", show_alert=True)
                return
            
            case.status = "closed"
            await case.save()
            await message.edit_text(f"Kasus `{case.title}` (ID: `{case_id}`) telah ditutup.")
            await callback_query.answer("Kasus ditutup.")

        # Contoh penanganan callback untuk monitoring keyword (admin)
        elif data.startswith("stop_monitor_"):
            parts = data.split("_")
            chat_id_str = parts[2]
            keyword = "_".join(parts[3:]) # Keyword bisa punya underscore
            
            try:
                target_chat_id = int(chat_id_str)
                from modules.admin.monitoring import KeywordMonitor # Import di sini untuk menghindari circular
                await KeywordMonitor.delete_monitor(chat_id=target_chat_id, keyword=keyword)
                await message.edit_text(f"Pemantauan kata kunci `{keyword}` di chat `{target_chat_id}` telah dihentikan.")
                await callback_query.answer("Pemantauan dihentikan.")
            except ValueError:
                await callback_query.answer("ID chat tidak valid.", show_alert=True)
            except Exception as e:
                log.error(f"Error stopping monitor via callback: {e}")
                await callback_query.answer("Gagal menghentikan pemantauan.", show_alert=True)

        else:
            await callback_query.answer("Aksi tidak dikenal.", show_alert=True)

    except Exception as e:
        log.error(f"Error handling callback query '{data}' from {user_id}: {e}")
        await callback_query.answer("Terjadi kesalahan saat memproses permintaan Anda.", show_alert=True)

