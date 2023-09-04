from .db import db
from .npc import NPC
import random

def add_npc(npc_data):
    npc = NPC(**npc_data)
    npc_dict = npc.to_dict()

    # Add the document to Firestore and get the auto-generated ID
    npc_ref = db.collection('npcs').document()
    npc_ref.set(npc_dict)
    npc_id = npc_ref.id

    # Update the document to include the ID field
    npc_dict["id"] = npc_id
    npc_ref.update({"id": npc_id})

    return npc_id

def get_all_npcs():
    npc_collection = db.collection("npcs").get()
    return [doc.to_dict() for doc in npc_collection]

def get_npc_by_id(npc_id):
    npc_ref = db.collection("npcs").document(npc_id)
    npc = npc_ref.get()
    return npc.to_dict() if npc.exists else None

def delete_npc_by_id(npc_id):
    npc_ref = db.collection("npcs").document(npc_id)
    npc = npc_ref.get()
    if npc.exists:
        npc_ref.delete()
        return True
    return False

def update_npc(npc_id, npc_data):
    npc = NPC(**npc_data)
    npc_dict = npc.to_dict()
    npc_ref = db.collection("npcs").document(npc_id)
    npc_ref.update(npc_dict)
    return npc_ref.id

def get_random_npc():
    npcs = get_all_npcs()
    return random.choice(npcs)