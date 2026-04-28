import json
import re

def parse_llm_response(result):
    try:
        # Mengambil konten dari dictionary response atau langsung dari result
        content = result.get("response") or result

        # 🔥 Logika pembersihan Markdown: hapus tag ```json ... ``` jika ada
        # Menjaga agar string JSON murni yang bisa di-load oleh library json
        content = re.sub(r"```json\n|\n```", "", content)

        parsed = json.loads(content)

        # Mengubah key pencarian dari "motivations" menjadi "pastries"
        # Tetap mengembalikan list kosong [] jika key tidak ditemukan
        return parsed.get("pastries", [])

    except Exception as e:
        # Tetap melempar exception dengan pesan yang jelas jika JSON tidak valid
        raise Exception(f"Invalid JSON from LLM: {str(e)}")