from datetime import UTC, datetime

from fern_labour_package_template.example import DomainEvent


def test_can_instantiate() -> None:
    event = DomainEvent(
        id="id123", type="test.event", data={"test": "data", "also": 123}, time=datetime.now(UTC)
    )
    assert isinstance(event, DomainEvent)

    cls_event = DomainEvent.create(data={"test": "data", "also": 123}, event_type="test.event")
    assert isinstance(cls_event, DomainEvent)


def test_can_serde_base_event() -> None:
    event = DomainEvent(
        id="id123", type="test.event", data={"test": "data", "also": 123}, time=datetime.now(UTC)
    )
    event_dict = event.to_dict()
    from_dict = DomainEvent.from_dict(event_dict)
    assert event == from_dict
