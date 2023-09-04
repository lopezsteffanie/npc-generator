from flask import Blueprint, jsonify, request
from .npc_service import add_npc, get_all_npcs, delete_npc_by_id, update_npc, get_random_npc, get_npc_by_id

npc_bp = Blueprint("npcs", __name__, url_prefix="/api")

@npc_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the NPC API!"}), 200

@npc_bp.route("/get-npc-by-id/<npc_id>", methods=["GET"])
def get_npc_by_id_route(npc_id):
    try:
        if npc := get_npc_by_id(npc_id):
            return jsonify(npc), 200
        else:
            return jsonify({"message": "NPC not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@npc_bp.route("/add-npc", methods=["POST"])
def add_npc_route():
    try:
        npc_data = request.get_json()
        npc_id = add_npc(npc_data)
        response = {
            "message": "NPC added successfully",
            "npc_id": npc_id
        }
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@npc_bp.route("/get-all-npcs", methods=["GET"])
def get_all_npcs_route():
    try:
        npcs = get_all_npcs()
        return jsonify(npcs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@npc_bp.route("/random", methods=["GET"])
def get_random_npc_route():
    try:
        npc = get_random_npc()
        return jsonify(npc), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@npc_bp.route("/delete-npc/<npc_id>", methods=["DELETE"])
def delete_npc_route(npc_id):
    try:
        if delete_npc_by_id(npc_id):
            return jsonify({"message": "NPC deleted successfully"}), 200
        else:
            return jsonify({"message": "NPC not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@npc_bp.route("/update-npc/<npc_id>", methods=["PATCH"])
def update_npc_route(npc_id):
    try:
        npc_data = request.get_json()
        npc_id = update_npc(npc_id, npc_data)
        response = {
            "message": "NPC updated successfully",
            "npc_id": npc_id
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500