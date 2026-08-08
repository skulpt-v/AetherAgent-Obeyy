from datetime import datetime, timezone
from pathlib import Path
import sqlite3


class Database:
    """AetherAgent'ın SQLite veritabanı yöneticisi."""

    def __init__(self, db_path: str = "data/aetheragent.db"):
        self.db_path = Path(db_path)

        # Veritabanının bulunduğu klasör yoksa oluştur.
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Veritabanı bağlantısını oluştur.
        # Streamlit farklı thread'ler kullandığı için
        # check_same_thread=False gerekli.
        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        # Foreign key kontrollerini etkinleştir.
        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        # Satırlara isimleriyle erişebilmek için.
        self.connection.row_factory = sqlite3.Row

        # Tabloları oluştur.
        self._create_tables()

    def _create_tables(self):
        """Gerekli SQLite tabloları oluşturur."""

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def _now(self) -> str:
        """UTC zamanını ISO 8601 formatında döndürür."""
        return datetime.now(timezone.utc).isoformat()

    def create_conversation(
        self,
        title: str = "Yeni Sohbet"
    ) -> int:
        """Yeni bir konuşma oluşturur ve ID'sini döndürür."""

        now = self._now()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO conversations (
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?)
            """,
            (title, now, now)
        )

        self.connection.commit()

        return cursor.lastrowid

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str
    ) -> int:
        """Bir konuşmaya yeni mesaj ekler ve mesaj ID'sini döndürür."""

        now = self._now()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages (
                conversation_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
                now
            )
        )

        # Konuşmanın son güncellenme zamanını yenile.
        cursor.execute(
            """
            UPDATE conversations
            SET updated_at = ?
            WHERE id = ?
            """,
            (
                now,
                conversation_id
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    def get_messages(
        self,
        conversation_id: int
    ):
        """Bir konuşmadaki tüm mesajları eskiden yeniye doğru getirir."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                conversation_id,
                role,
                content,
                created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        )

        return cursor.fetchall()

    def get_recent_messages(
        self,
        conversation_id: int,
        limit: int = 20
    ):
        """Bir konuşmanın son mesajlarını getirir."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                conversation_id,
                role,
                content,
                created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                conversation_id,
                limit
            )
        )

        messages = cursor.fetchall()

        # Veritabanından tersten geldiği için
        # tekrar eskiden yeniye sıralıyoruz.
        return list(reversed(messages))

    def get_latest_conversation(self):
        """En son oluşturulan konuşmayı getirir."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM conversations
            ORDER BY id DESC
            LIMIT 1
            """
        )

        return cursor.fetchone()

    def get_conversation(
        self,
        conversation_id: int
    ):
        """ID'si verilen konuşmanın bilgilerini getirir."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        return cursor.fetchone()

    # ==========================================================
    # KONUŞMA BAŞLIĞI GÜNCELLEME
    # ==========================================================

    def update_conversation_title(
        self,
        conversation_id: int,
        title: str
    ) -> bool:
        """Konuşmanın başlığını günceller."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (
                title,
                conversation_id
            )
        )

        self.connection.commit()

        return cursor.rowcount > 0

    # ==========================================================
    # KONUŞMA SİLME
    # ==========================================================

    def delete_conversation(
        self,
        conversation_id: int
    ) -> bool:
        """Konuşmayı ve bağlı mesajlarını siler."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        self.connection.commit()

        return cursor.rowcount > 0

    def save_memory(
        self,
        key: str,
        value: str,
        memory_type: str = "general",
        importance: float = 0.5
    ) -> int:
        """Yeni bir hafıza kaydeder ve ID'sini döndürür."""

        now = self._now()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories (
                key,
                value,
                memory_type,
                importance,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                key,
                value,
                memory_type,
                importance,
                now,
                now
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    def get_memories(self):
        """Kayıtlı tüm hafızaları getirir."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                key,
                value,
                memory_type,
                importance,
                created_at,
                updated_at
            FROM memories
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()

    def update_memory(
        self,
        memory_id: int,
        key: str,
        value: str,
        memory_type: str = "general",
        importance: float = 0.5
    ) -> bool:
        """Mevcut bir hafızayı günceller."""

        now = self._now()

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE memories
            SET
                key = ?,
                value = ?,
                memory_type = ?,
                importance = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                key,
                value,
                memory_type,
                importance,
                now,
                memory_id
            )
        )

        self.connection.commit()

        return cursor.rowcount > 0

    def delete_memory(
        self,
        memory_id: int
    ) -> bool:
        """Belirtilen hafızayı siler."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (memory_id,)
        )

        self.connection.commit()

        return cursor.rowcount > 0

    def close(self):
        """Veritabanı bağlantısını kapatır."""

        self.connection.close()

