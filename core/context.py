from memory import Database


class ContextManager:
    """AetherAgent'ın aktif konuşma bağlamını yönetir."""

    def __init__(self, database: Database):
        self.database = database

    def get_conversation_context(
        self,
        conversation_id: int,
        limit: int = 20
    ) -> str:
        """
        Konuşmanın son mesajlarını model için metin bağlamına dönüştürür.
        """

        messages = self.database.get_recent_messages(
            conversation_id,
            limit=limit
        )

        if not messages:
            return ""

        context_lines = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "user":
                speaker = "Kullanıcı"
            elif role == "assistant":
                speaker = "AetherAgent"
            else:
                speaker = role.capitalize()

            context_lines.append(
                f"{speaker}: {content}"
            )

        return "\n".join(context_lines)

    def build_context(
        self,
        conversation_id: int,
        limit: int = 20
    ) -> str:
        """
        Model için kullanılacak aktif konuşma bağlamını oluşturur.
        """

        return self.get_conversation_context(
            conversation_id,
            limit=limit
        )

