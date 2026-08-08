import logging

from groq import Groq

from config.settings import Config

# Streamlit Cloud'da dosyaya log yazmak yerine
# uygulamanın kendi log sistemini kullanıyoruz.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("LLM_Client")


class LLMClient:
    """Groq modeli ile iletişim kuran güvenli LLM istemcisi."""

    def __init__(self):
        # Ayarların doğruluğunu kontrol et.
        Config.validate()

        try:
            self.client = Groq(
                api_key=Config.GROQ_API_KEY
            )

            self.model_name = Config.MODEL_NAME

            logger.info(
                "Groq Client başarıyla başlatıldı ve API'ye bağlandı."
            )

        except Exception as error:
            logger.error(
                f"Groq Client başlatılırken hata oluştu: {error}"
            )
            raise

    def ask(
        self,
        prompt: str,
        system_instruction: str = None
    ) -> str:
        """
        Modele güvenli bir şekilde soru sorar
        ve yanıtı döndürür.
        """

        try:
            messages = []

            # Sistem talimatı varsa ilk mesaj olarak ekle.
            if system_instruction:
                messages.append({
                    "role": "system",
                    "content": system_instruction
                })

            # Kullanıcı isteğini ekle.
            messages.append({
                "role": "user",
                "content": prompt
            })

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7
            )

            if (
                response.choices
                and response.choices[0].message
                and response.choices[0].message.content
            ):
                return response.choices[0].message.content

            logger.warning(
                "Groq API'den boş bir yanıt döndü."
            )

            return (
                "Üzgünüm, boşluğa düştüm. "
                "Bu sorguya anlamlı bir yanıt üretemedim."
            )

        except Exception as error:
            error_message = (
                "API Bağlantı Hatası: "
                f"Sunucuyla iletişim kurulamadı. Detay: {error}"
            )

            logger.error(error_message)

            return error_message

