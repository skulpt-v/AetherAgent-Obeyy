import os

from dotenv import load_dotenv


# Çevresel değişkenleri yükle.
load_dotenv()


class Config:
    """Sistemin genel ayarlarını yöneten merkez."""

    # Groq API anahtarı.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Dizinler.
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    MEMORY_DIR = os.path.join(
        BASE_DIR,
        "memory"
    )

    LOGS_DIR = os.path.join(
        BASE_DIR,
        "logs"
    )

    # Veritabanı ve log.
    DB_PATH = os.path.join(
        MEMORY_DIR,
        "hafiza.db"
    )

    LOG_FILE = os.path.join(
        LOGS_DIR,
        "agent.log"
    )

    # Agent ayarları.
    AGENT_NAME = "Obeyy"

    # Groq üzerinde kullanılacak model.
    MODEL_NAME = "llama-3.3-70b-versatile"

    @classmethod
    def validate(cls):
        """Kritik sistem ayarlarını kontrol eder."""

        if not cls.GROQ_API_KEY:
            raise ValueError(
                "KRİTİK HATA: GROQ_API_KEY bulunamadı. "
                ".env dosyasını kontrol et."
            )

        # Gerekli klasörleri oluştur.
        os.makedirs(
            cls.MEMORY_DIR,
            exist_ok=True
        )

        os.makedirs(
            cls.LOGS_DIR,
            exist_ok=True
        )

        return True

