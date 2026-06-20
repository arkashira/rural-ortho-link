import json
from video_conferencing import VideoConferencing, Participant

def test_video_conferencing():
    conference = VideoConferencing()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    conference.add_participant(participant1)
    conference.add_participant(participant2)
    conference.start_conference()
    assert conference.verify_encryption()
    assert conference.verify_hipaa_compliance()
    assert len(conference.get_participants()) == 2

def test_video_conferencing_with_less_than_two_participants():
    conference = VideoConferencing()
    participant1 = Participant(1, "John")
    conference.add_participant(participant1)
    try:
        conference.start_conference()
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert str(e) == "At least 2 participants are required"

def test_video_conferencing_to_json():
    conference = VideoConferencing()
    participant1 = Participant(1, "John")
    participant2 = Participant(2, "Jane")
    conference.add_participant(participant1)
    conference.add_participant(participant2)
    conference.start_conference()
    json_data = conference.to_json()
    assert json.loads(json_data) == {
        "participants": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
        "encrypted": True,
        "hipaa_compliant": True
    }
