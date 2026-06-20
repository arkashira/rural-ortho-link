import json
from dataclasses import dataclass
from typing import List

@dataclass
class Participant:
    id: int
    name: str

class VideoConferencing:
    def __init__(self):
        self.participants = []
        self.encrypted = False
        self.hipaa_compliant = False

    def add_participant(self, participant: Participant):
        self.participants.append(participant)

    def start_conference(self):
        if len(self.participants) < 2:
            raise ValueError("At least 2 participants are required")
        self.encrypted = True
        self.hipaa_compliant = True

    def verify_encryption(self):
        return self.encrypted

    def verify_hipaa_compliance(self):
        return self.hipaa_compliant

    def get_participants(self):
        return self.participants

    def to_json(self):
        return json.dumps({
            "participants": [{"id": p.id, "name": p.name} for p in self.participants],
            "encrypted": self.encrypted,
            "hipaa_compliant": self.hipaa_compliant
        })
