from app.extensions import SessionLocal
from app.models.pastry import Pastry  # Mengasumsikan model sudah diubah menjadi Pastry
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_pastries(theme: str, total: int):
    session = SessionLocal()

    try:
        # Prompt disesuaikan untuk menghasilkan deskripsi pastry yang menggugah selera
        prompt = f"""
        Dalam format JSON, buat {total} deskripsi menu pastry yang menarik dengan tema "{theme}".
        Format:
        {{
            "pastries": [
                {{"text": "..."}}
            ]
        }}
        """

        result = generate_from_llm(prompt)
        pastries_data = parse_llm_response(result)

        # Simpan request log untuk audit atau tracking
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.commit()

        saved = []

        # Memproses setiap item pastry yang dihasilkan AI
        for item in pastries_data:
            text = item.get("text")

            p = Pastry(
                text=text,
                request_id=req_log.id
            )
            session.add(p)
            saved.append(text)

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_pastries(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Pastry)

        total_count = query.count()

        # Logika paginasi tetap dipertahankan sesuai modul praktikum [cite: 53, 171-177]
        data = (
            query
            .order_by(Pastry.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        # Format output JSON sesuai dengan kebutuhan Front-End [cite: 58-60, 521-525]
        result = [
            {
                "id": p.id,
                "text": p.text,
                "created_at": p.created_at.isoformat()
            }
            for p in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "total_pages": (total_count + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()