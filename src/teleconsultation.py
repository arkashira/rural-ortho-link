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
        print("Video conferencing started")

    def enable_end_to_end_encryption(self):
        self.encrypted = True
        # Simulate end-to-end encryption
        print("End-to-end encryption enabled")

    def document_hipaa_compliance(self):
        self.hipaa_compliant = True
        # Simulate HIPAA compliance documentation
        print("HIPAA compliance documented")

    def verify_acceptance_criteria(self):
        if len(self.participants) < 2:
            return False
        if not self.encrypted:
            return False
        if not self.hipaa_compliant:
            return False
        return True
