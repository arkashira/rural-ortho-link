import pytest
from teleconsultation import Teleconsultation, Participant

def test_add_participant():
    teleconsultation = Teleconsultation()
    participant = Participant(1, "John Doe")
    teleconsultation.add_participant(participant)
    assert len(teleconsultation.participants) == 1
    assert teleconsultation.participants[0].name == "John Doe"

def test_start_video_conferencing():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John Doe")
    participant2 = Participant(2, "Jane Doe")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    assert teleconsultation.start_video_conferencing() == "Video conferencing started"

def test_start_video_conferencing_with_less_than_two_participants():
    teleconsultation = Teleconsultation()
    participant = Participant(1, "John Doe")
    teleconsultation.add_participant(participant)
    with pytest.raises(ValueError):
        teleconsultation.start_video_conferencing()

def test_verify_end_to_end_encryption():
    teleconsultation = Teleconsultation()
    assert teleconsultation.verify_end_to_end_encryption() == "End-to-end encryption verified"
    assert teleconsultation.encrypted

def test_document_hipaa_compliance():
    teleconsultation = Teleconsultation()
    assert teleconsultation.document_hipaa_compliance() == "HIPAA compliance documented"
    assert teleconsultation.hipaa_compliant

def test_get_status():
    teleconsultation = Teleconsultation()
    participant1 = Participant(1, "John Doe")
    participant2 = Participant(2, "Jane Doe")
    teleconsultation.add_participant(participant1)
    teleconsultation.add_participant(participant2)
    teleconsultation.verify_end_to_end_encryption()
    teleconsultation.document_hipaa_compliance()
    status = teleconsultation.get_status()
    assert status["participants"] == ["John Doe", "Jane Doe"]
    assert status["encrypted"]
    assert status["hipaa_compliant"]
