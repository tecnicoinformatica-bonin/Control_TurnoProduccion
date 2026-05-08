from flask import jsonify
from . import api_bp

@api_bp.route('/health', methods=['GET'])
def health():
    """
    Health check del sistema
    ---
    responses:
      200:
        description: API funcionando correctamente
        examples:
          application/json:
            status: ok
            message: API Proyecto Turnos funcionando
    """
    return jsonify({
        "status": "ok",
        "message": "API Proycto Turnos funcionando"
    })