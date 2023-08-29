class NPC:
    def __init__(self, name, appearance, beliefs, secrets, extras=""):
        self.id = None
        self.name = name
        self.appearance = appearance
        self.beliefs = beliefs
        self.secrets = secrets
        self.extras = extras
        
    def to_dict(self):
        npc_dict = {
            "name": self.name,
            "appearance": self.appearance,
            "beliefs": self.beliefs,
            "secrets": self.secrets,
            "extras": self.extras
        }
        if self.id is not None:
            npc_dict["id"] = self.id
        return npc_dict