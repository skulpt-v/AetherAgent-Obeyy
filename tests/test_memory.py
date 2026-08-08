import os
import tempfile

import pytest

from memory import Database


@pytest.fixture
def database():
    """
    Her test için geçici bir SQLite veritabanı oluşturur.
    Test bittikten sonra dosya otomatik olarak silinir.
    """

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".db",
        delete=False,
    )

    temp_file.close()

    db = Database(temp_file.name)

    yield db

    try:
        db.connection.close()
    except Exception:
        pass

    try:
        os.remove(temp_file.name)
    except FileNotFoundError:
        pass


def test_create_conversation(database):
    conversation_id = database.create_conversation(
        title="Test Sohbeti"
    )

    assert conversation_id is not None

    conversation = database.get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation["title"] == "Test Sohbeti"


def test_update_conversation_title(database):
    conversation_id = database.create_conversation(
        title="Eski Başlık"
    )

    database.update_conversation_title(
        conversation_id=conversation_id,
        title="Yeni Başlık",
    )

    conversation = database.get_conversation(
        conversation_id
    )

    assert conversation["title"] == "Yeni Başlık"


def test_messages(database):
    conversation_id = database.create_conversation(
        title="Mesaj Testi"
    )

    database.add_message(
        conversation_id=conversation_id,
        role="user",
        content="Merhaba",
    )

    database.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content="Merhaba! Nasıl yardımcı olabilirim?",
    )

    messages = database.get_messages(
        conversation_id
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Merhaba"
    assert messages[1]["role"] == "assistant"


def test_delete_conversation(database):
    conversation_id = database.create_conversation(
        title="Silinecek Sohbet"
    )

    assert database.get_conversation(
        conversation_id
    ) is not None

    database.delete_conversation(
        conversation_id
    )

    assert database.get_conversation(
        conversation_id
    ) is None