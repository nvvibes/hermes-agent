from gateway.config import Platform
from gateway.platforms.base import MessageEvent, MessageType, coerce_plaintext_gateway_command
from gateway.session import SessionSource


def _source() -> SessionSource:
    return SessionSource(platform=Platform.MATTERMOST, chat_id="channel", chat_type="group")


def test_bang_clear_rewrites_to_new_in_group_chat():
    event = MessageEvent(
        text="!clear",
        message_type=MessageType.TEXT,
        source=_source(),
    )

    assert event.get_command() is None

    coerce_plaintext_gateway_command(event)

    assert event.text == "/new"
    assert event.is_command()
    assert event.get_command() == "new"


def test_bang_clear_rewrite_is_exact_and_case_insensitive():
    event = MessageEvent(
        text="  !CLEAR  ",
        message_type=MessageType.TEXT,
        source=_source(),
    )

    coerce_plaintext_gateway_command(event)

    assert event.text == "/new"


def test_bang_sentence_does_not_rewrite():
    event = MessageEvent(
        text="!that was surprising",
        message_type=MessageType.TEXT,
        source=_source(),
    )

    coerce_plaintext_gateway_command(event)

    assert event.text == "!that was surprising"
    assert event.get_command() is None
