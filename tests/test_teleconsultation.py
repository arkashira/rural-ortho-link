import pytest
from src.teleconsultation import Teleconsultation, Participant

def test_video_conferencing_with_two_participants():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    teleconsultation.start_video_conferencing()
    assert len(teleconsultation.participants) == 2

def test_video_conferencing_with_less_than_two_participants():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    teleconsultation.add_participant(participant1)
    with pytest.raises(ValueError):
        teleconsultation.start_video_conferencing()

def test_end_to_end_encryption():
    teleconsultation = Teleconsultation()
    teleconsultation.enable_end_to_end_encryption()
    assert teleconsultation.encrypted

def test_hipaa_compliance():
    teleconsultation = Teleconsultation()
    teleconsultation.document_hipaa_compliance()
    assert teleconsultation.hipaa_compliant

def test_verify_acceptance_criteria():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    teleconsultation.enable_end_to_end_encryption()
    teleconsultation.document_hipaa_compliance()
    assert teleconsultation.verify_acceptance_criteria()

def test_verify_acceptance_criteria_with_less_than_two_participants():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    teleconsultation.add_participant(participant1)
    teleconsultation.enable_end_to_end_encryption()
    teleconsultation.document_hipaa_compliance()
    assert not teleconsultation.verify_acceptance_criteria()

def test_verify_acceptance_criteria_without_end_to_end_encryption():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    teleconsultation.document_hipaa_compliance()
    assert not teleconsultation.verify_acceptance_criteria()

def test_verify_acceptance_criteria_without_hipaa_compliance():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    teleconsultation.enable_end_to_end_encryption()
    assert not teleconsultation.verify_acceptance_criteria()
