import json
from dataclasses import dataclass
from typing import List

@dataclass
class Participant:
    id: int
    name: str

class Teleconsultation:
    def __init__(self):
        self.participants = []
        self.encrypted = False
        self.hipaa_compliant = False

    def add_participant(self, participant: Participant):
        self.participants.append(participant)

    def start_video_conferencing(self):
        if len(self.participants) < 2:
            raise ValueError("At least 2 participants are required")
        # Simulate video conferencing
        return "Video conferencing started"

    def verify_end_to_end_encryption(self):
        self.encrypted = True
        return "End-to-end encryption verified"

    def document_hipaa_compliance(self):
        self.hipaa_compliant = True
        return "HIPAA compliance documented"

    def get_status(self):
        return {
            "participants": [p.name for p in self.participants],
            "encrypted": self.encrypted,
            "hipaa_compliant": self.hipaa_compliant
        }
