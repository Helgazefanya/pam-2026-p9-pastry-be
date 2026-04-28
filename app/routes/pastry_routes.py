from flask import Blueprint, request, jsonify
from app.services.pastry_service import (
    create_pastries,
    get_all_pastries
)

# Blueprint diubah dari pahlawan menjadi pastry
pastry_bp = Blueprint("pastry", __name__)

@pastry_bp.route("/", methods=["GET"])
def index():
    # Nama diperbarui menjadi Helga Zefanya Sipayung
    return "API telah berjalan! Dibuat oleh Helga Zefanya Sipayung"

@pastry_bp.route("/pastries/generate", methods=["POST"])
def generate():
    data = request.get_json()
    theme = data.get("theme")
    total = data.get("total")

    if not theme:
        return jsonify({"error": "Theme is required"}), 400
    
    if not total:
        return jsonify({"error": "Total is required"}), 400
    
    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400
    
    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_pastries(theme, total)

        return jsonify({
            "theme": theme,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pastry_bp.route("/pastries", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    data = get_all_pastries(page=page, per_page=per_page)

    return jsonify(data)