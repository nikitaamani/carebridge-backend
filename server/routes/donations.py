from flask import Blueprint

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/test', methods=['GET'])
def test():
    return {"message": "Donations route working!"}, 200
